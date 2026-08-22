#pragma once

#include "CoreMinimal.h"
#include "GameFramework/GameModeBase.h"
#include "LanDemoGameMode.generated.h"

UCLASS()
class UE5LANCONTROLDEMO_API ALanDemoGameMode : public AGameModeBase
{
    GENERATED_BODY()

public:
    ALanDemoGameMode();

protected:
    virtual void BeginPlay() override;
};
