using UnrealBuildTool;
using System.Collections.Generic;

public class UE5LanControlDemoEditorTarget : TargetRules
{
    public UE5LanControlDemoEditorTarget(TargetInfo Target) : base(Target)
    {
        Type = TargetType.Editor;
        DefaultBuildSettings = BuildSettingsVersion.V5;
        IncludeOrderVersion = EngineIncludeOrderVersion.Unreal5_4;
        ExtraModuleNames.Add("UE5LanControlDemo");
    }
}
