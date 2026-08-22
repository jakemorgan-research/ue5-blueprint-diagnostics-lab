#include "LanDemoPlayerController.h"

#include "BlueprintLanSubsystem.h"
#include "Engine/Engine.h"
#include "Engine/GameViewportClient.h"
#include "Misc/CommandLine.h"
#include "Misc/Parse.h"
#include "Widgets/Input/SButton.h"
#include "Widgets/Input/SEditableTextBox.h"
#include "Widgets/Layout/SBorder.h"
#include "Widgets/Layout/SBox.h"
#include "Widgets/Layout/SUniformGridPanel.h"
#include "Widgets/SBoxPanel.h"
#include "Widgets/SOverlay.h"
#include "Widgets/SWeakWidget.h"
#include "Widgets/Text/STextBlock.h"

ALanDemoPlayerController::ALanDemoPlayerController()
{
    PrimaryActorTick.bCanEverTick = true;
}

void ALanDemoPlayerController::Tick(float DeltaSeconds)
{
    Super::Tick(DeltaSeconds);

    if (!bControllerModeActive || HeldAxis.IsNearlyZero())
    {
        return;
    }

    CommandHeartbeatSeconds += DeltaSeconds;
    if (CommandHeartbeatSeconds >= 0.1f)
    {
        CommandHeartbeatSeconds = 0.0f;
        if (UBlueprintLanSubsystem* Lan = GetGameInstance()->GetSubsystem<UBlueprintLanSubsystem>())
        {
            if (Lan->IsLanConnected())
            {
                Lan->SendMoveCommand(HeldAxis);
            }
        }
    }
}

void ALanDemoPlayerController::BeginPlay()
{
    Super::BeginPlay();

    if (UBlueprintLanSubsystem* Lan = GetGameInstance()->GetSubsystem<UBlueprintLanSubsystem>())
    {
        Lan->OnStatusMessage.AddDynamic(this, &ALanDemoPlayerController::HandleStatus);
        Lan->OnConnectionChanged.AddDynamic(this, &ALanDemoPlayerController::HandleConnectionChanged);
    }

    const bool bControllerMode = FParse::Param(FCommandLine::Get(), TEXT("lancontroller"));
#if PLATFORM_ANDROID
    bControllerModeActive = true;
    BuildControllerUI();
#else
    if (bControllerMode)
    {
        bControllerModeActive = true;
        BuildControllerUI();
    }
    else if (GEngine)
    {
        GEngine->AddOnScreenDebugMessage(-1, 15.0f, FColor::Green,
            TEXT("Desktop server listening on TCP 7777. Launch another build with -lancontroller."));
    }
#endif
}

void ALanDemoPlayerController::EndPlay(const EEndPlayReason::Type EndPlayReason)
{
    if (RootWidget.IsValid() && GEngine && GEngine->GameViewport)
    {
        GEngine->GameViewport->RemoveViewportWidgetContent(RootWidget.ToSharedRef());
    }
    RootWidget.Reset();
    Super::EndPlay(EndPlayReason);
}

void ALanDemoPlayerController::BuildControllerUI()
{
    bShowMouseCursor = true;
    SetInputMode(FInputModeUIOnly());

    TSharedRef<SWidget> Panel =
        SNew(SBorder)
        .Padding(24.0f)
        [
            SNew(SVerticalBox)
            + SVerticalBox::Slot().AutoHeight().Padding(4.0f)
            [
                SNew(STextBlock).Text(FText::FromString(TEXT("UE5 LAN Controller")))
            ]
            + SVerticalBox::Slot().AutoHeight().Padding(4.0f)
            [
                SAssignNew(AddressBox, SEditableTextBox)
                .Text(FText::FromString(TEXT("127.0.0.1")))
                .HintText(FText::FromString(TEXT("Desktop IPv4 address")))
            ]
            + SVerticalBox::Slot().AutoHeight().Padding(4.0f)
            [
                SNew(SButton)
                .Text(FText::FromString(TEXT("Connect")))
                .OnClicked_Lambda([this]() { return ConnectClicked(); })
            ]
            + SVerticalBox::Slot().AutoHeight().Padding(4.0f)
            [
                SAssignNew(StatusText, STextBlock)
                .Text(FText::FromString(TEXT("Disconnected")))
            ]
            + SVerticalBox::Slot().AutoHeight().Padding(4.0f)
            [
                SNew(SUniformGridPanel)
                + SUniformGridPanel::Slot(1, 0)
                [
                    SNew(SButton).Text(FText::FromString(TEXT("Forward")))
                    .OnPressed_Lambda([this]() { SendAxis(FVector2D(0.0f, 1.0f)); })
                    .OnReleased_Lambda([this]() { SendStop(); })
                ]
                + SUniformGridPanel::Slot(0, 1)
                [
                    SNew(SButton).Text(FText::FromString(TEXT("Left")))
                    .OnPressed_Lambda([this]() { SendAxis(FVector2D(-1.0f, 0.0f)); })
                    .OnReleased_Lambda([this]() { SendStop(); })
                ]
                + SUniformGridPanel::Slot(1, 1)
                [
                    SNew(SButton).Text(FText::FromString(TEXT("Stop")))
                    .OnClicked_Lambda([this]() { return SendStop(); })
                ]
                + SUniformGridPanel::Slot(2, 1)
                [
                    SNew(SButton).Text(FText::FromString(TEXT("Right")))
                    .OnPressed_Lambda([this]() { SendAxis(FVector2D(1.0f, 0.0f)); })
                    .OnReleased_Lambda([this]() { SendStop(); })
                ]
                + SUniformGridPanel::Slot(1, 2)
                [
                    SNew(SButton).Text(FText::FromString(TEXT("Back")))
                    .OnPressed_Lambda([this]() { SendAxis(FVector2D(0.0f, -1.0f)); })
                    .OnReleased_Lambda([this]() { SendStop(); })
                ]
            ]
        ];

    RootWidget = SNew(SWeakWidget).PossiblyNullContent(Panel);
    if (GEngine && GEngine->GameViewport)
    {
        GEngine->GameViewport->AddViewportWidgetContent(RootWidget.ToSharedRef(), 100);
    }
}

FReply ALanDemoPlayerController::ConnectClicked()
{
    if (UBlueprintLanSubsystem* Lan = GetGameInstance()->GetSubsystem<UBlueprintLanSubsystem>())
    {
        const FString Address = AddressBox.IsValid() ? AddressBox->GetText().ToString() : TEXT("127.0.0.1");
        Lan->ConnectToLanServer(Address, 7777);
    }
    return FReply::Handled();
}

FReply ALanDemoPlayerController::SendAxis(FVector2D Axis)
{
    HeldAxis = Axis;
    CommandHeartbeatSeconds = 0.0f;
    if (UBlueprintLanSubsystem* Lan = GetGameInstance()->GetSubsystem<UBlueprintLanSubsystem>())
    {
        Lan->SendMoveCommand(Axis);
    }
    return FReply::Handled();
}

FReply ALanDemoPlayerController::SendStop()
{
    HeldAxis = FVector2D::ZeroVector;
    CommandHeartbeatSeconds = 0.0f;
    if (UBlueprintLanSubsystem* Lan = GetGameInstance()->GetSubsystem<UBlueprintLanSubsystem>())
    {
        Lan->SendStopCommand();
    }
    return FReply::Handled();
}

void ALanDemoPlayerController::HandleStatus(const FString& Message)
{
    if (StatusText.IsValid())
    {
        StatusText->SetText(FText::FromString(Message));
    }
}

void ALanDemoPlayerController::HandleConnectionChanged(bool bConnected)
{
    HandleStatus(bConnected ? TEXT("Connected") : TEXT("Disconnected"));
}
