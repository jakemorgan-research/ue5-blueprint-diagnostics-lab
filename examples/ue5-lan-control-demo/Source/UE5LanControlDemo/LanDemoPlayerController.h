#pragma once

#include "CoreMinimal.h"
#include "GameFramework/PlayerController.h"
#include "LanDemoPlayerController.generated.h"

class SEditableTextBox;
class STextBlock;
class SWidget;

UCLASS()
class UE5LANCONTROLDEMO_API ALanDemoPlayerController : public APlayerController
{
    GENERATED_BODY()

public:
    ALanDemoPlayerController();
    virtual void Tick(float DeltaSeconds) override;

protected:
    virtual void BeginPlay() override;
    virtual void EndPlay(const EEndPlayReason::Type EndPlayReason) override;

private:
    void BuildControllerUI();
    FReply ConnectClicked();
    FReply SendAxis(FVector2D Axis);
    FReply SendStop();

    UFUNCTION()
    void HandleStatus(const FString& Message);

    UFUNCTION()
    void HandleConnectionChanged(bool bConnected);

    TSharedPtr<SEditableTextBox> AddressBox;
    TSharedPtr<STextBlock> StatusText;
    TSharedPtr<SWidget> RootWidget;
    FVector2D HeldAxis = FVector2D::ZeroVector;
    float CommandHeartbeatSeconds = 0.0f;
    bool bControllerModeActive = false;
};
