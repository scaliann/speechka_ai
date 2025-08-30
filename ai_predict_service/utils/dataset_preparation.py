import os
import shutil

# Путь к исходному датасету
source_dir = r"C:\Users\coolp\Downloads\child_defects_dataset"

# Путь к целевой папке
target_dir = r"C:\speechka_classification\wavfiles"

# Важно: порядок меток — от длинных к коротким
label_map = [
    ('_lispandburr', 'lisp_burr'),
    ('_burr', 'burr'),
    ('_lisp', 'lisp'),
    ('_healthy', 'healthy'),
]

# Создание папок назначения
for _, folder in label_map:
    os.makedirs(os.path.join(target_dir, folder), exist_ok=True)

# Проход по папкам пациентов
for patient_folder in os.listdir(source_dir):
    patient_path = os.path.join(source_dir, patient_folder)

    if os.path.isdir(patient_path):
        for file in os.listdir(patient_path):
            if file.lower().endswith('.wav'):
                file_path = os.path.join(patient_path, file)

                label_found = False

                for label, folder in label_map:
                    if label in file:
                        label_found = True
                        target_path = os.path.join(target_dir, folder, file)

                        # Проверка на дубли
                        if os.path.exists(target_path):
                            base, ext = os.path.splitext(file)
                            new_file_name = f"{patient_folder}_{base}{ext}"
                            target_path = os.path.join(target_dir, folder, new_file_name)

                        shutil.copy2(file_path, target_path)
                        print(f"Скопировано: {file} -> {folder}")
                        break

                if not label_found:
                    print(f"метка не найдена для файла: {file}")

print('Копирование завершено.')
