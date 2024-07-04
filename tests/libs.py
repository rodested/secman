def are_files_equal(file_path1, file_path2):
    with open(file_path1, 'rb') as file1, open(file_path2, 'rb') as file2:
        content1 = file1.read()
        content2 = file2.read()
        return content1 == content2
