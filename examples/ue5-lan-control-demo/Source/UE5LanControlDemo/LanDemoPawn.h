#pragma once

#include "CoreMinimal.h"
#include "GameFramework/Pawn.h"
#include "LanDemoPawn.generated.h"

class UCameraComponent;
class USpringArmComponent;
class UStaticMeshComponent;

UCLASS()
class UE5LANCONTROLDEMO_API ALanDemoPawn : public APawn
{
    GENERATED_BODY()

public:
    ALanDemoPawn();
    virtual void Tick(float DeltaSeconds) override;

protected:
    virtual void BeginPlay() override;

private:
    UFUNCTION()
    void HandleMoveCommand(FVector2D Axis, int32 Sequence);

    UPROPERTY(VisibleAnywhere)
    TObjectPtr<UStaticMeshComponent> Mesh;

    UPROPERTY(VisibleAnywhere)
    TObjectPtr<USpringArmComponent> SpringArm;

    UPROPERTY(VisibleAnywhere)
    TObjectPtr<UCameraComponent> Camera;

    FVector2D CurrentAxis = FVector2D::ZeroVector;
    float MoveSpeed = 350.0f;
};
