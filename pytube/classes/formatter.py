import inquirer


class VideoFormatter:
    @staticmethod
    def select_format(preferred_formats):
        """Allow user to select a format using arrow keys."""
        if not preferred_formats:
            print("No preferred formats available.")
            return None

        # Prepare the choices for inquirer
        choices = [
            f"ID: {fmt_id}, Quality: {info['format_note']}, "
            f"Audio: {'Yes' if info['has_audio'] else 'No'}, "
            f"Size: {round((info['filesize']) / (1024 * 1024), 2)} MB" if info['filesize'] != "Unknown" else
            f"ID: {fmt_id}, Quality: {info['format_note']}, Audio: {'Yes' if info['has_audio'] else 'No'}, Size: Unknown"
            for fmt_id, info in preferred_formats.items()
        ]

        # Ask user to select a format
        question = [
            inquirer.List(
                "format",
                message="Select the format to download:",
                choices=choices
            )
        ]
        answer = inquirer.prompt(question)
        if answer:
            # Extract the selected format ID from the choice
            selected = answer["format"]
            format_id = selected.split(",")[0].split(":")[1].strip()
            
            # Print the selected format
            print(f"\nYou have selected the following format:\n{selected}\n")
            return format_id
        return None