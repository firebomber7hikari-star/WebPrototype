#if UNITY_IOS
using System.IO;
using UnityEditor;
using UnityEditor.Callbacks;
using UnityEditor.iOS.Xcode;

namespace FindDifferences.EditorTools
{
    /// <summary>
    /// Declares in Info.plist that the app uses no non-exempt encryption (ITSAppUsesNonExemptEncryption = NO, shown in Xcode
    /// as "App Uses Non-Exempt Encryption: NO"), so App Store Connect does not ask the export-compliance question per build.
    /// </summary>
    public static class FDEncryptionBuild
    {
        [PostProcessBuild(100)]
        static void OnPostProcessBuild(BuildTarget target, string path)
        {
            if (target != BuildTarget.iOS) return;
            string plistPath = Path.Combine(path, "Info.plist");
            var plist = new PlistDocument();
            plist.ReadFromFile(plistPath);
            plist.root.SetBoolean("ITSAppUsesNonExemptEncryption", false);
            plist.WriteToFile(plistPath);
        }
    }
}
#endif
