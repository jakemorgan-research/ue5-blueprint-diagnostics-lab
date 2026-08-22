#pragma once

#include "CoreMinimal.h"
#include "Subsystems/GameInstanceSubsystem.h"
#include "BlueprintLanSubsystem.generated.h"

class FSocket;

DECLARE_DYNAMIC_MULTICAST_DELEGATE_OneParam(FBETConnectionChanged, bool, bConnected);
DECLARE_DYNAMIC_MULTICAST_DELEGATE_TwoParams(FBETMoveCommand, FVector2D, Axis, int32, Sequence);
DECLARE_DYNAMIC_MULTICAST_DELEGATE_OneParam(FBETStatusMessage, const FString&, Message);

UCLASS()
class BLUEPRINTENGINEERINGTOOLKIT_API UBlueprintLanSubsystem : public UGameInstanceSubsystem
{
    GENERATED_BODY()

public:
    virtual void Initialize(FSubsystemCollectionBase& Collection) override;
    virtual void Deinitialize() override;

    UPROPERTY(BlueprintAssignable, Category="Blueprint Engineering Toolkit|LAN")
    FBETConnectionChanged OnConnectionChanged;

    UPROPERTY(BlueprintAssignable, Category="Blueprint Engineering Toolkit|LAN")
    FBETMoveCommand OnMoveCommand;

    UPROPERTY(BlueprintAssignable, Category="Blueprint Engineering Toolkit|LAN")
    FBETStatusMessage OnStatusMessage;

    UFUNCTION(BlueprintCallable, Category="Blueprint Engineering Toolkit|LAN")
    bool StartLanServer(int32 Port = 7777);

    UFUNCTION(BlueprintCallable, Category="Blueprint Engineering Toolkit|LAN")
    void StopLanServer();

    UFUNCTION(BlueprintCallable, Category="Blueprint Engineering Toolkit|LAN")
    bool ConnectToLanServer(const FString& IPv4Address, int32 Port = 7777);

    UFUNCTION(BlueprintCallable, Category="Blueprint Engineering Toolkit|LAN")
    void DisconnectLanClient();

    UFUNCTION(BlueprintCallable, Category="Blueprint Engineering Toolkit|LAN")
    bool SendMoveCommand(FVector2D Axis);

    UFUNCTION(BlueprintCallable, Category="Blueprint Engineering Toolkit|LAN")
    bool SendStopCommand();

    UFUNCTION(BlueprintPure, Category="Blueprint Engineering Toolkit|LAN")
    bool IsLanConnected() const;

    UFUNCTION(BlueprintPure, Category="Blueprint Engineering Toolkit|LAN")
    FString GetLanStatus() const { return Status; }

private:
    bool Tick(float DeltaSeconds);
    void PumpListener();
    void PumpSocket(FSocket* Socket, TArray<uint8>& Buffer, bool bFromClient);
    void ParseLine(const FString& Line, bool bFromClient);
    bool SendJsonLine(FSocket* Socket, const FString& Line);
    void CloseSocket(FSocket*& Socket);
    void SetStatus(const FString& NewStatus);

    FSocket* ListenerSocket = nullptr;
    FSocket* PeerSocket = nullptr;
    FSocket* ClientSocket = nullptr;
    TArray<uint8> PeerBuffer;
    TArray<uint8> ClientBuffer;
    FTSTicker::FDelegateHandle TickHandle;
    FString Status = TEXT("Idle");
    int32 NextSequence = 1;
    double LastMotionCommandSeconds = 0.0;
    bool bMotionActive = false;
};
