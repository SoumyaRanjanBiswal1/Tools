import os

# 🔧 Specify the folder path here
folder_path = r"path\to\your\folder"

def count_lines_in_python_files(folder):
    file_line_counts = {}
    
    for root, _, files in os.walk(folder):
        for file in files:
            if file.endswith(".py"):
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, "r", encoding="utf-8") as f:
                        lines = f.readlines()
                        file_line_counts[file_path] = len(lines)
                except Exception as e:
                    print(f"Error reading {file_path}: {e}")
    
    return file_line_counts

def save_report(file_line_counts):
    sorted_files = sorted(file_line_counts.items(), key=lambda x: x[1], reverse=True)
    total_lines = sum(count for _, count in sorted_files)

    report_path = os.path.join(os.getcwd(), "code_line_report.txt")
    with open(report_path, "w", encoding="utf-8") as report:
        report.write("Python Code Line Report\n")
        report.write("========================\n\n")
        for file_path, line_count in sorted_files:
            report.write(f"{file_path}: {line_count} lines\n")
        report.write("\n========================\n")
        report.write(f"Total Lines of Code: {total_lines}\n")
    
    print(f"\n✅ Report saved to: {report_path}")
    print(f"📊 Total Python lines in all files: {total_lines}")

if __name__ == "__main__":
    file_line_counts = count_lines_in_python_files(folder_path)
    save_report(file_line_counts)
