using UnrealBuildTool;

public class BlueprintEngineeringToolkit : ModuleRules
{
    public BlueprintEngineeringToolkit(ReadOnlyTargetRules Target) : base(Target)
    {
        PCHUsage = PCHUsageMode.UseExplicitOrSharedPCHs;

        PublicDependencyModuleNames.AddRange(new[]
        {
            "Core",
            "CoreUObject",
            "Engine",
            "Json",
            "Networking",
            "Sockets"
        });
    }
}
