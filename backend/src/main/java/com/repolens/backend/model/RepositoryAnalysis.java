package com.repolens.backend.model;

public class RepositoryAnalysis {

    private Long repositoryId;
    private String repositoryName;
    private int totalFiles;
    private int javaFiles;
    private int javascriptFiles;

    public RepositoryAnalysis(
            Long repositoryId,
            String repositoryName,
            int totalFiles,
            int javaFiles,
            int javascriptFiles) {

        this.repositoryId = repositoryId;
        this.repositoryName = repositoryName;
        this.totalFiles = totalFiles;
        this.javaFiles = javaFiles;
        this.javascriptFiles = javascriptFiles;
    }

    public Long getRepositoryId() {
        return repositoryId;
    }

    public String getRepositoryName() {
        return repositoryName;
    }

    public int getTotalFiles() {
        return totalFiles;
    }

    public int getJavaFiles() {
        return javaFiles;
    }

    public int getJavascriptFiles() {
        return javascriptFiles;
    }
}