on run {iconPath, title, message}
    tell application "System Events"
        display notification message with image alias (POSIX path of iconPath)
    end tell
end run