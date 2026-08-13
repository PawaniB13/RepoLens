package com.repolens.backend.model;

public class RepositoryAnalysis {

    private Long repositoryId;
    private String repositoryName;
    private int totalFiles;
    private int javaFiles;
    private int javascriptFiles;

    public RepositoryAnalysis() {
    }

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

    public void setRepositoryId(Long repositoryId) {
        this.repositoryId = repositoryId;
    }

    public String getRepositoryName() {
        return repositoryName;
    }

    public void setRepositoryName(String repositoryName) {
        this.repositoryName = repositoryName;
    }

    public int getTotalFiles() {
        return totalFiles;
    }

    public void setTotalFiles(int totalFiles) {
        this.totalFiles = totalFiles;
    }

    public int getJavaFiles() {
        return javaFiles;
    }

    public void setJavaFiles(int javaFiles) {
        this.javaFiles = javaFiles;
    }

    public int getJavascriptFiles() {
        return javascriptFiles;
    }

    public void setJavascriptFiles(int javascriptFiles) {
        this.javascriptFiles = javascriptFiles;
    }
}