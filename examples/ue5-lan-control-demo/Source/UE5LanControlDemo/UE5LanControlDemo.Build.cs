using UnrealBuildTool;

public class UE5LanControlDemo : ModuleRules
{
    public UE5LanControlDemo(ReadOnlyTargetRules Target) : base(Target)
    {
        PCHUsage = PCHUsageMode.UseExplicitOrSharedPCHs;

        PublicDependencyModuleNames.AddRange(new[]
        {
            "Core",
            "CoreUObject",
            "Engine",
            "InputCore",
            "Slate",
            "SlateCore",
            "UMG",
            "BlueprintEngineeringToolkit"
        });
    }
}
