#!/usr/bin/env ruby

# CodeQuest MVP - Xcode Project Generator
# Creates a complete .xcodeproj file structure

require 'securerandom'
require 'fileutils'

PROJECT_NAME = "CodeQuestMVP"
PROJECT_DIR = "/Users/lottebecking/Documents/GitHub/dream-space-microsoft/CodeQuestMVP"
BUNDLE_ID = "com.lottebecking.CodeQuestMVP"

# Generate unique UUIDs for Xcode objects
def uuid
  SecureRandom.uuid.gsub('-', '').upcase[0..23]
end

# File structure
swift_files = [
  "CodeQuestMVPApp.swift",
  "Models/Block.swift",
  "Models/Mission.swift",
  "Models/Level.swift",
  "Models/User.swift",
  "ViewModels/GameProgressViewModel.swift",
  "ViewModels/MissionViewModel.swift",
  "Services/BlockExecutor.swift",
  "Views/MainMenuView.swift",
  "Views/MissionView.swift",
  "Views/SimulationView.swift",
  "Views/WorkspaceView.swift",
  "Views/BlockPaletteView.swift",
  "Views/LevelSelectionView.swift",
  "Views/MissionListView.swift",
  "Views/ProgressView.swift",
  "SampleData/SampleData.swift"
]

# Generate file references
file_refs = {}
swift_files.each { |f| file_refs[f] = uuid }
info_plist_ref = uuid
assets_ref = uuid

# Generate build file references
build_files = {}
swift_files.each { |f| build_files[f] = uuid }

# Group UUIDs
main_group = uuid
products_group = uuid
models_group = uuid
viewmodels_group = uuid
services_group = uuid
views_group = uuid
sampledata_group = uuid

# Target & Project UUIDs
target_uuid = uuid
project_uuid = uuid
sources_phase = uuid
resources_phase = uuid
frameworks_phase = uuid
product_ref = uuid
config_list_project = uuid
config_list_target = uuid
debug_config = uuid
release_config = uuid
debug_config_target = uuid
release_config_target = uuid

puts "🎨 Generating Xcode project for #{PROJECT_NAME}..."

# Create .xcodeproj directory
xcodeproj_dir = "#{PROJECT_DIR}/#{PROJECT_NAME}.xcodeproj"
FileUtils.mkdir_p(xcodeproj_dir)

# Generate project.pbxproj content
pbxproj_content = <<-PBXPROJ
// !$*UTF8*$!
{
	archiveVersion = 1;
	classes = {
	};
	objectVersion = 55;
	objects = {

/* Begin PBXBuildFile section */
PBXPROJ

swift_files.each do |file|
  pbxproj_content += "\t\t#{build_files[file]} /* #{File.basename(file)} in Sources */ = {isa = PBXBuildFile; fileRef = #{file_refs[file]} /* #{File.basename(file)} */; };\n"
end

pbxproj_content += <<-PBXPROJ
/* End PBXBuildFile section */

/* Begin PBXFileReference section */
		#{product_ref} /* #{PROJECT_NAME}.app */ = {isa = PBXFileReference; explicitFileType = wrapper.application; includeInIndex = 0; path = #{PROJECT_NAME}.app; sourceTree = BUILT_PRODUCTS_DIR; };
		#{info_plist_ref} /* Info.plist */ = {isa = PBXFileReference; lastKnownFileType = text.plist.xml; path = Info.plist; sourceTree = "<group>"; };
PBXPROJ

swift_files.each do |file|
  basename = File.basename(file)
  pbxproj_content += "\t\t#{file_refs[file]} /* #{basename} */ = {isa = PBXFileReference; lastKnownFileType = sourcecode.swift; path = #{basename}; sourceTree = \"<group>\"; };\n"
end

pbxproj_content += <<-PBXPROJ
/* End PBXFileReference section */

/* Begin PBXFrameworksBuildPhase section */
		#{frameworks_phase} /* Frameworks */ = {
			isa = PBXFrameworksBuildPhase;
			buildActionMask = 2147483647;
			files = (
			);
			runOnlyForDeploymentPostprocessing = 0;
		};
/* End PBXFrameworksBuildPhase section */

/* Begin PBXGroup section */
		#{main_group} = {
			isa = PBXGroup;
			children = (
				#{file_refs["CodeQuestMVPApp.swift"]} /* CodeQuestMVPApp.swift */,
				#{models_group} /* Models */,
				#{viewmodels_group} /* ViewModels */,
				#{services_group} /* Services */,
				#{views_group} /* Views */,
				#{sampledata_group} /* SampleData */,
				#{info_plist_ref} /* Info.plist */,
				#{products_group} /* Products */,
			);
			sourceTree = "<group>";
		};
		#{products_group} /* Products */ = {
			isa = PBXGroup;
			children = (
				#{product_ref} /* #{PROJECT_NAME}.app */,
			);
			name = Products;
			sourceTree = "<group>";
		};
		#{models_group} /* Models */ = {
			isa = PBXGroup;
			children = (
				#{file_refs["Models/Block.swift"]} /* Block.swift */,
				#{file_refs["Models/Mission.swift"]} /* Mission.swift */,
				#{file_refs["Models/Level.swift"]} /* Level.swift */,
				#{file_refs["Models/User.swift"]} /* User.swift */,
			);
			path = Models;
			sourceTree = "<group>";
		};
		#{viewmodels_group} /* ViewModels */ = {
			isa = PBXGroup;
			children = (
				#{file_refs["ViewModels/GameProgressViewModel.swift"]} /* GameProgressViewModel.swift */,
				#{file_refs["ViewModels/MissionViewModel.swift"]} /* MissionViewModel.swift */,
			);
			path = ViewModels;
			sourceTree = "<group>";
		};
		#{services_group} /* Services */ = {
			isa = PBXGroup;
			children = (
				#{file_refs["Services/BlockExecutor.swift"]} /* BlockExecutor.swift */,
			);
			path = Services;
			sourceTree = "<group>";
		};
		#{views_group} /* Views */ = {
			isa = PBXGroup;
			children = (
				#{file_refs["Views/MainMenuView.swift"]} /* MainMenuView.swift */,
				#{file_refs["Views/MissionView.swift"]} /* MissionView.swift */,
				#{file_refs["Views/SimulationView.swift"]} /* SimulationView.swift */,
				#{file_refs["Views/WorkspaceView.swift"]} /* WorkspaceView.swift */,
				#{file_refs["Views/BlockPaletteView.swift"]} /* BlockPaletteView.swift */,
				#{file_refs["Views/LevelSelectionView.swift"]} /* LevelSelectionView.swift */,
				#{file_refs["Views/MissionListView.swift"]} /* MissionListView.swift */,
				#{file_refs["Views/ProgressView.swift"]} /* ProgressView.swift */,
			);
			path = Views;
			sourceTree = "<group>";
		};
		#{sampledata_group} /* SampleData */ = {
			isa = PBXGroup;
			children = (
				#{file_refs["SampleData/SampleData.swift"]} /* SampleData.swift */,
			);
			path = SampleData;
			sourceTree = "<group>";
		};
/* End PBXGroup section */

/* Begin PBXNativeTarget section */
		#{target_uuid} /* #{PROJECT_NAME} */ = {
			isa = PBXNativeTarget;
			buildConfigurationList = #{config_list_target} /* Build configuration list for PBXNativeTarget "#{PROJECT_NAME}" */;
			buildPhases = (
				#{sources_phase} /* Sources */,
				#{frameworks_phase} /* Frameworks */,
				#{resources_phase} /* Resources */,
			);
			buildRules = (
			);
			dependencies = (
			);
			name = #{PROJECT_NAME};
			productName = #{PROJECT_NAME};
			productReference = #{product_ref} /* #{PROJECT_NAME}.app */;
			productType = "com.apple.product-type.application";
		};
/* End PBXNativeTarget section */

/* Begin PBXProject section */
		#{project_uuid} /* Project object */ = {
			isa = PBXProject;
			attributes = {
				BuildIndependentTargetsInParallel = 1;
				LastSwiftUpdateCheck = 1400;
				LastUpgradeCheck = 1400;
				TargetAttributes = {
					#{target_uuid} = {
						CreatedOnToolsVersion = 14.0;
					};
				};
			};
			buildConfigurationList = #{config_list_project} /* Build configuration list for PBXProject "#{PROJECT_NAME}" */;
			compatibilityVersion = "Xcode 13.0";
			developmentRegion = en;
			hasScannedForEncodings = 0;
			knownRegions = (
				en,
				Base,
			);
			mainGroup = #{main_group};
			productRefGroup = #{products_group} /* Products */;
			projectDirPath = "";
			projectRoot = "";
			targets = (
				#{target_uuid} /* #{PROJECT_NAME} */,
			);
		};
/* End PBXProject section */

/* Begin PBXResourcesBuildPhase section */
		#{resources_phase} /* Resources */ = {
			isa = PBXResourcesBuildPhase;
			buildActionMask = 2147483647;
			files = (
			);
			runOnlyForDeploymentPostprocessing = 0;
		};
/* End PBXResourcesBuildPhase section */

/* Begin PBXSourcesBuildPhase section */
		#{sources_phase} /* Sources */ = {
			isa = PBXSourcesBuildPhase;
			buildActionMask = 2147483647;
			files = (
PBXPROJ

swift_files.each do |file|
  pbxproj_content += "\t\t\t\t#{build_files[file]} /* #{File.basename(file)} in Sources */,\n"
end

pbxproj_content += <<-PBXPROJ
			);
			runOnlyForDeploymentPostprocessing = 0;
		};
/* End PBXSourcesBuildPhase section */

/* Begin XCBuildConfiguration section */
		#{debug_config} /* Debug */ = {
			isa = XCBuildConfiguration;
			buildSettings = {
				ALWAYS_SEARCH_USER_PATHS = NO;
				CLANG_ANALYZER_NONNULL = YES;
				CLANG_ANALYZER_NUMBER_OBJECT_CONVERSION = YES_AGGRESSIVE;
				CLANG_CXX_LANGUAGE_STANDARD = "gnu++20";
				CLANG_ENABLE_MODULES = YES;
				CLANG_ENABLE_OBJC_ARC = YES;
				CLANG_ENABLE_OBJC_WEAK = YES;
				CLANG_WARN_BLOCK_CAPTURE_AUTORELEASING = YES;
				CLANG_WARN_BOOL_CONVERSION = YES;
				CLANG_WARN_COMMA = YES;
				CLANG_WARN_CONSTANT_CONVERSION = YES;
				CLANG_WARN_DEPRECATED_OBJC_IMPLEMENTATIONS = YES;
				CLANG_WARN_DIRECT_OBJC_ISA_USAGE = YES_ERROR;
				CLANG_WARN_DOCUMENTATION_COMMENTS = YES;
				CLANG_WARN_EMPTY_BODY = YES;
				CLANG_WARN_ENUM_CONVERSION = YES;
				CLANG_WARN_INFINITE_RECURSION = YES;
				CLANG_WARN_INT_CONVERSION = YES;
				CLANG_WARN_NON_LITERAL_NULL_CONVERSION = YES;
				CLANG_WARN_OBJC_IMPLICIT_RETAIN_SELF = YES;
				CLANG_WARN_OBJC_LITERAL_CONVERSION = YES;
				CLANG_WARN_OBJC_ROOT_CLASS = YES_ERROR;
				CLANG_WARN_QUOTED_INCLUDE_IN_FRAMEWORK_HEADER = YES;
				CLANG_WARN_RANGE_LOOP_ANALYSIS = YES;
				CLANG_WARN_STRICT_PROTOTYPES = YES;
				CLANG_WARN_SUSPICIOUS_MOVE = YES;
				CLANG_WARN_UNGUARDED_AVAILABILITY = YES_AGGRESSIVE;
				CLANG_WARN_UNREACHABLE_CODE = YES;
				CLANG_WARN__DUPLICATE_METHOD_MATCH = YES;
				COPY_PHASE_STRIP = NO;
				DEBUG_INFORMATION_FORMAT = dwarf;
				ENABLE_STRICT_OBJC_MSGSEND = YES;
				ENABLE_TESTABILITY = YES;
				GCC_C_LANGUAGE_STANDARD = gnu11;
				GCC_DYNAMIC_NO_PIC = NO;
				GCC_NO_COMMON_BLOCKS = YES;
				GCC_OPTIMIZATION_LEVEL = 0;
				GCC_PREPROCESSOR_DEFINITIONS = (
					"DEBUG=1",
					"$(inherited)",
				);
				GCC_WARN_64_TO_32_BIT_CONVERSION = YES;
				GCC_WARN_ABOUT_RETURN_TYPE = YES_ERROR;
				GCC_WARN_UNDECLARED_SELECTOR = YES;
				GCC_WARN_UNINITIALIZED_AUTOS = YES_AGGRESSIVE;
				GCC_WARN_UNUSED_FUNCTION = YES;
				GCC_WARN_UNUSED_VARIABLE = YES;
				IPHONEOS_DEPLOYMENT_TARGET = 15.0;
				MTL_ENABLE_DEBUG_INFO = INCLUDE_SOURCE;
				MTL_FAST_MATH = YES;
				ONLY_ACTIVE_ARCH = YES;
				SDKROOT = iphoneos;
				SWIFT_ACTIVE_COMPILATION_CONDITIONS = DEBUG;
				SWIFT_OPTIMIZATION_LEVEL = "-Onone";
			};
			name = Debug;
		};
		#{release_config} /* Release */ = {
			isa = XCBuildConfiguration;
			buildSettings = {
				ALWAYS_SEARCH_USER_PATHS = NO;
				CLANG_ANALYZER_NONNULL = YES;
				CLANG_ANALYZER_NUMBER_OBJECT_CONVERSION = YES_AGGRESSIVE;
				CLANG_CXX_LANGUAGE_STANDARD = "gnu++20";
				CLANG_ENABLE_MODULES = YES;
				CLANG_ENABLE_OBJC_ARC = YES;
				CLANG_ENABLE_OBJC_WEAK = YES;
				CLANG_WARN_BLOCK_CAPTURE_AUTORELEASING = YES;
				CLANG_WARN_BOOL_CONVERSION = YES;
				CLANG_WARN_COMMA = YES;
				CLANG_WARN_CONSTANT_CONVERSION = YES;
				CLANG_WARN_DEPRECATED_OBJC_IMPLEMENTATIONS = YES;
				CLANG_WARN_DIRECT_OBJC_ISA_USAGE = YES_ERROR;
				CLANG_WARN_DOCUMENTATION_COMMENTS = YES;
				CLANG_WARN_EMPTY_BODY = YES;
				CLANG_WARN_ENUM_CONVERSION = YES;
				CLANG_WARN_INFINITE_RECURSION = YES;
				CLANG_WARN_INT_CONVERSION = YES;
				CLANG_WARN_NON_LITERAL_NULL_CONVERSION = YES;
				CLANG_WARN_OBJC_IMPLICIT_RETAIN_SELF = YES;
				CLANG_WARN_OBJC_LITERAL_CONVERSION = YES;
				CLANG_WARN_OBJC_ROOT_CLASS = YES_ERROR;
				CLANG_WARN_QUOTED_INCLUDE_IN_FRAMEWORK_HEADER = YES;
				CLANG_WARN_RANGE_LOOP_ANALYSIS = YES;
				CLANG_WARN_STRICT_PROTOTYPES = YES;
				CLANG_WARN_SUSPICIOUS_MOVE = YES;
				CLANG_WARN_UNGUARDED_AVAILABILITY = YES_AGGRESSIVE;
				CLANG_WARN_UNREACHABLE_CODE = YES;
				CLANG_WARN__DUPLICATE_METHOD_MATCH = YES;
				COPY_PHASE_STRIP = NO;
				DEBUG_INFORMATION_FORMAT = "dwarf-with-dsym";
				ENABLE_NS_ASSERTIONS = NO;
				ENABLE_STRICT_OBJC_MSGSEND = YES;
				GCC_C_LANGUAGE_STANDARD = gnu11;
				GCC_NO_COMMON_BLOCKS = YES;
				GCC_WARN_64_TO_32_BIT_CONVERSION = YES;
				GCC_WARN_ABOUT_RETURN_TYPE = YES_ERROR;
				GCC_WARN_UNDECLARED_SELECTOR = YES;
				GCC_WARN_UNINITIALIZED_AUTOS = YES_AGGRESSIVE;
				GCC_WARN_UNUSED_FUNCTION = YES;
				GCC_WARN_UNUSED_VARIABLE = YES;
				IPHONEOS_DEPLOYMENT_TARGET = 15.0;
				MTL_ENABLE_DEBUG_INFO = NO;
				MTL_FAST_MATH = YES;
				SDKROOT = iphoneos;
				SWIFT_COMPILATION_MODE = wholemodule;
				SWIFT_OPTIMIZATION_LEVEL = "-O";
				VALIDATE_PRODUCT = YES;
			};
			name = Release;
		};
		#{debug_config_target} /* Debug */ = {
			isa = XCBuildConfiguration;
			buildSettings = {
				ASSETCATALOG_COMPILER_APPICON_NAME = AppIcon;
				ASSETCATALOG_COMPILER_GLOBAL_ACCENT_COLOR_NAME = AccentColor;
				CODE_SIGN_STYLE = Automatic;
				CURRENT_PROJECT_VERSION = 1;
				DEVELOPMENT_TEAM = "";
				ENABLE_PREVIEWS = YES;
				GENERATE_INFOPLIST_FILE = YES;
				INFOPLIST_FILE = Info.plist;
				INFOPLIST_KEY_CFBundleDisplayName = "CodeQuest MVP";
				INFOPLIST_KEY_UIApplicationSceneManifest_Generation = YES;
				INFOPLIST_KEY_UIApplicationSupportsIndirectInputEvents = YES;
				INFOPLIST_KEY_UILaunchScreen_Generation = YES;
				INFOPLIST_KEY_UISupportedInterfaceOrientations = "UIInterfaceOrientationPortrait UIInterfaceOrientationLandscapeLeft UIInterfaceOrientationLandscapeRight";
				INFOPLIST_KEY_UISupportedInterfaceOrientations_iPad = "UIInterfaceOrientationPortrait UIInterfaceOrientationPortraitUpsideDown UIInterfaceOrientationLandscapeLeft UIInterfaceOrientationLandscapeRight";
				INFOPLIST_KEY_UISupportedInterfaceOrientations_iPhone = "UIInterfaceOrientationPortrait UIInterfaceOrientationLandscapeLeft UIInterfaceOrientationLandscapeRight";
				LD_RUNPATH_SEARCH_PATHS = (
					"$(inherited)",
					"@executable_path/Frameworks",
				);
				MARKETING_VERSION = 1.0;
				PRODUCT_BUNDLE_IDENTIFIER = "#{BUNDLE_ID}";
				PRODUCT_NAME = "$(TARGET_NAME)";
				SWIFT_EMIT_LOC_STRINGS = YES;
				SWIFT_VERSION = 5.0;
				TARGETED_DEVICE_FAMILY = "1,2";
			};
			name = Debug;
		};
		#{release_config_target} /* Release */ = {
			isa = XCBuildConfiguration;
			buildSettings = {
				ASSETCATALOG_COMPILER_APPICON_NAME = AppIcon;
				ASSETCATALOG_COMPILER_GLOBAL_ACCENT_COLOR_NAME = AccentColor;
				CODE_SIGN_STYLE = Automatic;
				CURRENT_PROJECT_VERSION = 1;
				DEVELOPMENT_TEAM = "";
				ENABLE_PREVIEWS = YES;
				GENERATE_INFOPLIST_FILE = YES;
				INFOPLIST_FILE = Info.plist;
				INFOPLIST_KEY_CFBundleDisplayName = "CodeQuest MVP";
				INFOPLIST_KEY_UIApplicationSceneManifest_Generation = YES;
				INFOPLIST_KEY_UIApplicationSupportsIndirectInputEvents = YES;
				INFOPLIST_KEY_UILaunchScreen_Generation = YES;
				INFOPLIST_KEY_UISupportedInterfaceOrientations = "UIInterfaceOrientationPortrait UIInterfaceOrientationLandscapeLeft UIInterfaceOrientationLandscapeRight";
				INFOPLIST_KEY_UISupportedInterfaceOrientations_iPad = "UIInterfaceOrientationPortrait UIInterfaceOrientationPortraitUpsideDown UIInterfaceOrientationLandscapeLeft UIInterfaceOrientationLandscapeRight";
				INFOPLIST_KEY_UISupportedInterfaceOrientations_iPhone = "UIInterfaceOrientationPortrait UIInterfaceOrientationLandscapeLeft UIInterfaceOrientationLandscapeRight";
				LD_RUNPATH_SEARCH_PATHS = (
					"$(inherited)",
					"@executable_path/Frameworks",
				);
				MARKETING_VERSION = 1.0;
				PRODUCT_BUNDLE_IDENTIFIER = "#{BUNDLE_ID}";
				PRODUCT_NAME = "$(TARGET_NAME)";
				SWIFT_EMIT_LOC_STRINGS = YES;
				SWIFT_VERSION = 5.0;
				TARGETED_DEVICE_FAMILY = "1,2";
			};
			name = Release;
		};
/* End XCBuildConfiguration section */

/* Begin XCConfigurationList section */
		#{config_list_project} /* Build configuration list for PBXProject "#{PROJECT_NAME}" */ = {
			isa = XCConfigurationList;
			buildConfigurations = (
				#{debug_config} /* Debug */,
				#{release_config} /* Release */,
			);
			defaultConfigurationIsVisible = 0;
			defaultConfigurationName = Release;
		};
		#{config_list_target} /* Build configuration list for PBXNativeTarget "#{PROJECT_NAME}" */ = {
			isa = XCConfigurationList;
			buildConfigurations = (
				#{debug_config_target} /* Debug */,
				#{release_config_target} /* Release */,
			);
			defaultConfigurationIsVisible = 0;
			defaultConfigurationName = Release;
		};
/* End XCConfigurationList section */
	};
	rootObject = #{project_uuid} /* Project object */;
}
PBXPROJ

# Write project.pbxproj
File.write("#{xcodeproj_dir}/project.pbxproj", pbxproj_content)

# Create xcshareddata directory for schemes
xcshareddata_dir = "#{xcodeproj_dir}/xcshareddata/xcschemes"
FileUtils.mkdir_p(xcshareddata_dir)

# Create scheme file
scheme_content = <<-SCHEME
<?xml version="1.0" encoding="UTF-8"?>
<Scheme
   LastUpgradeVersion = "1400"
   version = "1.3">
   <BuildAction
      parallelizeBuildables = "YES"
      buildImplicitDependencies = "YES">
      <BuildActionEntries>
         <BuildActionEntry
            buildForTesting = "YES"
            buildForRunning = "YES"
            buildForProfiling = "YES"
            buildForArchiving = "YES"
            buildForAnalyzing = "YES">
            <BuildableReference
               BuildableIdentifier = "primary"
               BlueprintIdentifier = "#{target_uuid}"
               BuildableName = "#{PROJECT_NAME}.app"
               BlueprintName = "#{PROJECT_NAME}"
               ReferencedContainer = "container:#{PROJECT_NAME}.xcodeproj">
            </BuildableReference>
         </BuildActionEntry>
      </BuildActionEntries>
   </BuildAction>
   <TestAction
      buildConfiguration = "Debug"
      selectedDebuggerIdentifier = "Xcode.DebuggerFoundation.Debugger.LLDB"
      selectedLauncherIdentifier = "Xcode.DebuggerFoundation.Launcher.LLDB"
      shouldUseLaunchSchemeArgsEnv = "YES">
      <Testables>
      </Testables>
   </TestAction>
   <LaunchAction
      buildConfiguration = "Debug"
      selectedDebuggerIdentifier = "Xcode.DebuggerFoundation.Debugger.LLDB"
      selectedLauncherIdentifier = "Xcode.DebuggerFoundation.Launcher.LLDB"
      launchStyle = "0"
      useCustomWorkingDirectory = "NO"
      ignoresPersistentStateOnLaunch = "NO"
      debugDocumentVersioning = "YES"
      debugServiceExtension = "internal"
      allowLocationSimulation = "YES">
      <BuildableProductRunnable
         runnableDebuggingMode = "0">
         <BuildableReference
            BuildableIdentifier = "primary"
            BlueprintIdentifier = "#{target_uuid}"
            BuildableName = "#{PROJECT_NAME}.app"
            BlueprintName = "#{PROJECT_NAME}"
            ReferencedContainer = "container:#{PROJECT_NAME}.xcodeproj">
         </BuildableReference>
      </BuildableProductRunnable>
   </LaunchAction>
   <ProfileAction
      buildConfiguration = "Release"
      shouldUseLaunchSchemeArgsEnv = "YES"
      savedToolIdentifier = ""
      useCustomWorkingDirectory = "NO"
      debugDocumentVersioning = "YES">
      <BuildableProductRunnable
         runnableDebuggingMode = "0">
         <BuildableReference
            BuildableIdentifier = "primary"
            BlueprintIdentifier = "#{target_uuid}"
            BuildableName = "#{PROJECT_NAME}.app"
            BlueprintName = "#{PROJECT_NAME}"
            ReferencedContainer = "container:#{PROJECT_NAME}.xcodeproj">
         </BuildableReference>
      </BuildableProductRunnable>
   </ProfileAction>
   <AnalyzeAction
      buildConfiguration = "Debug">
   </AnalyzeAction>
   <ArchiveAction
      buildConfiguration = "Release"
      revealArchiveInOrganizer = "YES">
   </ArchiveAction>
</Scheme>
SCHEME

File.write("#{xcshareddata_dir}/#{PROJECT_NAME}.xcscheme", scheme_content)

# Create workspace settings
workspace_settings_dir = "#{xcodeproj_dir}/project.xcworkspace"
FileUtils.mkdir_p("#{workspace_settings_dir}/xcshareddata")

workspace_content = <<-WORKSPACE
<?xml version="1.0" encoding="UTF-8"?>
<Workspace
   version = "1.0">
   <FileRef
      location = "self:">
   </FileRef>
</Workspace>
WORKSPACE

File.write("#{workspace_settings_dir}/contents.xcworkspacedata", workspace_content)

puts "✅ Xcode project created successfully!"
puts ""
puts "📂 Project location:"
puts "   #{xcodeproj_dir}"
puts ""
puts "🚀 To open in Xcode:"
puts "   open #{PROJECT_NAME}.xcodeproj"
puts ""
puts "   Or double-click: #{PROJECT_NAME}.xcodeproj"
puts ""
