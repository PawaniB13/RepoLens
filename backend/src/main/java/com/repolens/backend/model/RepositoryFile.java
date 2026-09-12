package com.repolens.backend.model;

public class RepositoryFile {

    private String fileName;
    private String fileType;
    private String path;

    public RepositoryFile() {
    }

    public RepositoryFile(
            String fileName,
            String fileType,
            String path) {

        this.fileName = fileName;
        this.fileType = fileType;
        this.path = path;
    }

    public String getFileName() {
        return fileName;
    }

    public void setFileName(String fileName) {
        this.fileName = fileName;
    }

    public String getFileType() {
        return fileType;
    }

    public void setFileType(String fileType) {
        this.fileType = fileType;
    }

    public String getPath() {
        return path;
    }

    public void setPath(String path) {
        this.path = path;
    }
}