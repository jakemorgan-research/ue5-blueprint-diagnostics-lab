#include "BlueprintLanSubsystem.h"

#include "Common/TcpSocketBuilder.h"
#include "Dom/JsonObject.h"
#include "HAL/PlatformTime.h"
#include "Interfaces/IPv4/IPv4Address.h"
#include "Serialization/JsonReader.h"
#include "Serialization/JsonSerializer.h"
#include "SocketSubsystem.h"
#include "Sockets.h"

namespace
{
    constexpr int32 MaxMessageBytes = 4096;
    constexpr int32 ReceiveChunkBytes = 2048;

    FVector2D ClampAxis(FVector2D Axis)
    {
        Axis.X = FMath::Clamp(Axis.X, -1.0, 1.0);
        Axis.Y = FMath::Clamp(Axis.Y, -1.0, 1.0);
        return Axis.SizeSquared() > 1.0 ? Axis.GetSafeNormal() : Axis;
    }
}

void UBlueprintLanSubsystem::Initialize(FSubsystemCollectionBase& Collection)
{
    Super::Initialize(Collection);
    TickHandle = FTSTicker::GetCoreTicker().AddTicker(
        FTickerDelegate::CreateUObject(this, &UBlueprintLanSubsystem::Tick));
}

void UBlueprintLanSubsystem::Deinitialize()
{
    FTSTicker::GetCoreTicker().RemoveTicker(TickHandle);
    DisconnectLanClient();
    StopLanServer();
    Super::Deinitialize();
}

bool UBlueprintLanSubsystem::StartLanServer(int32 Port)
{
    StopLanServer();
    if (Port < 1 || Port > 65535)
    {
        SetStatus(TEXT("Invalid server port"));
        return false;
    }

    ListenerSocket = FTcpSocketBuilder(TEXT("BET_LAN_Server"))
        .AsReusable()
        .BoundToPort(Port)
        .Listening(4)
        .WithReceiveBufferSize(MaxMessageBytes * 4);

    if (!ListenerSocket)
    {
        SetStatus(TEXT("Unable to start LAN server"));
        return false;
    }

    ListenerSocket->SetNonBlocking(true);
    SetStatus(FString::Printf(TEXT("Server listening on TCP %d"), Port));
    return true;
}

void UBlueprintLanSubsystem::StopLanServer()
{
    const bool bHadPeer = PeerSocket != nullptr;
    if (bMotionActive)
    {
        OnMoveCommand.Broadcast(FVector2D::ZeroVector, NextSequence++);
        bMotionActive = false;
    }
    CloseSocket(PeerSocket);
    CloseSocket(ListenerSocket);
    PeerBuffer.Reset();
    if (bHadPeer)
    {
        OnConnectionChanged.Broadcast(false);
    }
}

bool UBlueprintLanSubsystem::ConnectToLanServer(const FString& IPv4Address, int32 Port)
{
    DisconnectLanClient();

    FIPv4Address ParsedAddress;
    if (!FIPv4Address::Parse(IPv4Address, ParsedAddress) || Port < 1 || Port > 65535)
    {
        SetStatus(TEXT("Enter a valid IPv4 address and port"));
        return false;
    }

    ISocketSubsystem* SocketSubsystem = ISocketSubsystem::Get(PLATFORM_SOCKETSUBSYSTEM);
    TSharedRef<FInternetAddr> RemoteAddress = SocketSubsystem->CreateInternetAddr();
    RemoteAddress->SetIp(ParsedAddress.Value);
    RemoteAddress->SetPort(Port);

    ClientSocket = FTcpSocketBuilder(TEXT("BET_LAN_Client"))
        .WithReceiveBufferSize(MaxMessageBytes * 4)
        .WithSendBufferSize(MaxMessageBytes * 4);

    if (!ClientSocket || !ClientSocket->Connect(*RemoteAddress))
    {
        CloseSocket(ClientSocket);
        SetStatus(TEXT("Connection failed"));
        OnConnectionChanged.Broadcast(false);
        return false;
    }

    ClientSocket->SetNonBlocking(true);
    SetStatus(TEXT("Connected"));
    OnConnectionChanged.Broadcast(true);
    return true;
}

void UBlueprintLanSubsystem::DisconnectLanClient()
{
    const bool bWasConnected = ClientSocket != nullptr;
    CloseSocket(ClientSocket);
    ClientBuffer.Reset();
    if (bWasConnected)
    {
        SetStatus(TEXT("Disconnected"));
        OnConnectionChanged.Broadcast(false);
    }
}

bool UBlueprintLanSubsystem::SendMoveCommand(FVector2D Axis)
{
    if (!ClientSocket)
    {
        SetStatus(TEXT("Connect before sending commands"));
        return false;
    }

    Axis = ClampAxis(Axis);
    const int32 Sequence = NextSequence++;
    const FString Line = FString::Printf(
        TEXT("{\"v\":1,\"type\":\"move\",\"x\":%.3f,\"y\":%.3f,\"seq\":%d}"),
        Axis.X, Axis.Y, Sequence);
    return SendJsonLine(ClientSocket, Line);
}

bool UBlueprintLanSubsystem::SendStopCommand()
{
    if (!ClientSocket)
    {
        SetStatus(TEXT("Connect before sending commands"));
        return false;
    }

    const FString Line = FString::Printf(
        TEXT("{\"v\":1,\"type\":\"stop\",\"seq\":%d}"), NextSequence++);
    return SendJsonLine(ClientSocket, Line);
}

bool UBlueprintLanSubsystem::IsLanConnected() const
{
    return ClientSocket != nullptr || PeerSocket != nullptr;
}

bool UBlueprintLanSubsystem::Tick(float DeltaSeconds)
{
    PumpListener();
    PumpSocket(PeerSocket, PeerBuffer, true);
    PumpSocket(ClientSocket, ClientBuffer, false);

    if (PeerSocket && PeerSocket->GetConnectionState() == SCS_ConnectionError)
    {
        CloseSocket(PeerSocket);
        PeerBuffer.Reset();
        if (bMotionActive)
        {
            bMotionActive = false;
            OnMoveCommand.Broadcast(FVector2D::ZeroVector, NextSequence++);
        }
        SetStatus(TEXT("Controller disconnected"));
        OnConnectionChanged.Broadcast(false);
    }

    if (ClientSocket && ClientSocket->GetConnectionState() == SCS_ConnectionError)
    {
        CloseSocket(ClientSocket);
        ClientBuffer.Reset();
        SetStatus(TEXT("Server disconnected"));
        OnConnectionChanged.Broadcast(false);
    }

    if (bMotionActive && FPlatformTime::Seconds() - LastMotionCommandSeconds > 0.5)
    {
        bMotionActive = false;
        OnMoveCommand.Broadcast(FVector2D::ZeroVector, NextSequence++);
        SetStatus(TEXT("Fail-safe stop: command timeout"));
    }
    return true;
}

void UBlueprintLanSubsystem::PumpListener()
{
    if (!ListenerSocket)
    {
        return;
    }

    bool bHasPendingConnection = false;
    if (ListenerSocket->HasPendingConnection(bHasPendingConnection) && bHasPendingConnection)
    {
        CloseSocket(PeerSocket);
        PeerSocket = ListenerSocket->Accept(TEXT("BET_LAN_Peer"));
        if (PeerSocket)
        {
            PeerSocket->SetNonBlocking(true);
            PeerBuffer.Reset();
            SetStatus(TEXT("Controller connected"));
            OnConnectionChanged.Broadcast(true);
        }
    }
}

void UBlueprintLanSubsystem::PumpSocket(FSocket* Socket, TArray<uint8>& Buffer, bool bFromClient)
{
    if (!Socket)
    {
        return;
    }

    uint32 PendingBytes = 0;
    while (Socket->HasPendingData(PendingBytes))
    {
        const int32 Requested = FMath::Min<int32>(ReceiveChunkBytes, static_cast<int32>(PendingBytes));
        uint8 Chunk[ReceiveChunkBytes];
        int32 BytesRead = 0;
        if (!Socket->Recv(Chunk, Requested, BytesRead) || BytesRead <= 0)
        {
            break;
        }
        Buffer.Append(Chunk, BytesRead);
        if (Buffer.Num() > MaxMessageBytes)
        {
            Buffer.Reset();
            SetStatus(TEXT("Rejected oversized LAN message"));
            return;
        }
    }

    int32 NewlineIndex = INDEX_NONE;
    while (Buffer.Find(static_cast<uint8>('\n'), NewlineIndex))
    {
        TArray<uint8> LineBytes;
        LineBytes.Append(Buffer.GetData(), NewlineIndex);
        Buffer.RemoveAt(0, NewlineIndex + 1, EAllowShrinking::No);
        LineBytes.Add(0);
        ParseLine(UTF8_TO_TCHAR(reinterpret_cast<const char*>(LineBytes.GetData())), bFromClient);
    }
}

void UBlueprintLanSubsystem::ParseLine(const FString& Line, bool bFromClient)
{
    TSharedPtr<FJsonObject> Json;
    const TSharedRef<TJsonReader<>> Reader = TJsonReaderFactory<>::Create(Line);
    if (!FJsonSerializer::Deserialize(Reader, Json) || !Json.IsValid())
    {
        SetStatus(TEXT("Rejected malformed JSON"));
        return;
    }

    double Version = 0.0;
    FString Type;
    double SequenceNumber = 0.0;
    if (!Json->TryGetNumberField(TEXT("v"), Version) || Version != 1.0 ||
        !Json->TryGetStringField(TEXT("type"), Type) ||
        !Json->TryGetNumberField(TEXT("seq"), SequenceNumber))
    {
        SetStatus(TEXT("Rejected unsupported command"));
        return;
    }

    const int32 Sequence = static_cast<int32>(SequenceNumber);
    if (bFromClient && Type == TEXT("move"))
    {
        double X = 0.0;
        double Y = 0.0;
        if (Json->TryGetNumberField(TEXT("x"), X) && Json->TryGetNumberField(TEXT("y"), Y))
        {
            const FVector2D Axis = ClampAxis(FVector2D(X, Y));
            OnMoveCommand.Broadcast(Axis, Sequence);
            bMotionActive = !Axis.IsNearlyZero();
            LastMotionCommandSeconds = FPlatformTime::Seconds();
            SendJsonLine(PeerSocket, FString::Printf(TEXT("{\"v\":1,\"type\":\"ack\",\"seq\":%d}"), Sequence));
        }
    }
    else if (bFromClient && Type == TEXT("stop"))
    {
        OnMoveCommand.Broadcast(FVector2D::ZeroVector, Sequence);
        bMotionActive = false;
        SendJsonLine(PeerSocket, FString::Printf(TEXT("{\"v\":1,\"type\":\"ack\",\"seq\":%d}"), Sequence));
    }
    else if (!bFromClient && Type == TEXT("ack"))
    {
        SetStatus(FString::Printf(TEXT("Command %d acknowledged"), Sequence));
    }
}

bool UBlueprintLanSubsystem::SendJsonLine(FSocket* Socket, const FString& Line)
{
    if (!Socket || Line.Len() > MaxMessageBytes)
    {
        return false;
    }

    const FString Framed = Line + TEXT("\n");
    FTCHARToUTF8 Payload(*Framed);
    int32 TotalSent = 0;
    while (TotalSent < Payload.Length())
    {
        int32 SentNow = 0;
        if (!Socket->Send(
                reinterpret_cast<const uint8*>(Payload.Get()) + TotalSent,
                Payload.Length() - TotalSent,
                SentNow) || SentNow <= 0)
        {
            SetStatus(TEXT("Send failed"));
            return false;
        }
        TotalSent += SentNow;
    }
    return true;
}

void UBlueprintLanSubsystem::CloseSocket(FSocket*& Socket)
{
    if (!Socket)
    {
        return;
    }

    Socket->Close();
    if (ISocketSubsystem* SocketSubsystem = ISocketSubsystem::Get(PLATFORM_SOCKETSUBSYSTEM))
    {
        SocketSubsystem->DestroySocket(Socket);
    }
    Socket = nullptr;
}

void UBlueprintLanSubsystem::SetStatus(const FString& NewStatus)
{
    Status = NewStatus;
    OnStatusMessage.Broadcast(Status);
}
