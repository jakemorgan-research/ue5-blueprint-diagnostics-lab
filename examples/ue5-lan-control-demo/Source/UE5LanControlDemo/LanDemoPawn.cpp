#include "LanDemoPawn.h"

#include "BlueprintLanSubsystem.h"
#include "Camera/CameraComponent.h"
#include "Components/StaticMeshComponent.h"
#include "Engine/StaticMesh.h"
#include "GameFramework/SpringArmComponent.h"
#include "UObject/ConstructorHelpers.h"

ALanDemoPawn::ALanDemoPawn()
{
    PrimaryActorTick.bCanEverTick = true;

    Mesh = CreateDefaultSubobject<UStaticMeshComponent>(TEXT("DemoMesh"));
    SetRootComponent(Mesh);

    static ConstructorHelpers::FObjectFinder<UStaticMesh> CubeAsset(TEXT("/Engine/BasicShapes/Cube.Cube"));
    if (CubeAsset.Succeeded())
    {
        Mesh->SetStaticMesh(CubeAsset.Object);
    }
    Mesh->SetWorldScale3D(FVector(0.75f));

    SpringArm = CreateDefaultSubobject<USpringArmComponent>(TEXT("SpringArm"));
    SpringArm->SetupAttachment(Mesh);
    SpringArm->TargetArmLength = 900.0f;
    SpringArm->SetRelativeRotation(FRotator(-35.0f, -45.0f, 0.0f));

    Camera = CreateDefaultSubobject<UCameraComponent>(TEXT("Camera"));
    Camera->SetupAttachment(SpringArm);
}

void ALanDemoPawn::BeginPlay()
{
    Super::BeginPlay();

    if (UBlueprintLanSubsystem* Lan = GetGameInstance()->GetSubsystem<UBlueprintLanSubsystem>())
    {
        Lan->OnMoveCommand.AddDynamic(this, &ALanDemoPawn::HandleMoveCommand);
    }
}

void ALanDemoPawn::Tick(float DeltaSeconds)
{
    Super::Tick(DeltaSeconds);

    const FVector Delta(CurrentAxis.Y, CurrentAxis.X, 0.0f);
    AddActorWorldOffset(Delta * MoveSpeed * DeltaSeconds, true);
}

void ALanDemoPawn::HandleMoveCommand(FVector2D Axis, int32 Sequence)
{
    CurrentAxis = Axis.SizeSquared() > 1.0 ? Axis.GetSafeNormal() : Axis;
}
