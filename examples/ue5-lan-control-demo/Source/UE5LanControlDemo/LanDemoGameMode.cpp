#include "LanDemoGameMode.h"

#include "BlueprintLanSubsystem.h"
#include "LanDemoPawn.h"
#include "LanDemoPlayerController.h"
#include "Misc/CommandLine.h"
#include "Misc/Parse.h"

ALanDemoGameMode::ALanDemoGameMode()
{
    DefaultPawnClass = ALanDemoPawn::StaticClass();
    PlayerControllerClass = ALanDemoPlayerController::StaticClass();
}

void ALanDemoGameMode::BeginPlay()
{
    Super::BeginPlay();

    const bool bControllerMode = FParse::Param(FCommandLine::Get(), TEXT("lancontroller"));
#if PLATFORM_ANDROID
    const bool bShouldHost = false;
#else
    const bool bShouldHost = !bControllerMode;
#endif

    if (bShouldHost)
    {
        if (UBlueprintLanSubsystem* Lan = GetGameInstance()->GetSubsystem<UBlueprintLanSubsystem>())
        {
            Lan->StartLanServer(7777);
        }
    }
}
