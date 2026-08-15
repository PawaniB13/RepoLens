package com.repolens.backend.model;

public class RepositoryStatistics {

    private Long repositoryId;
    private String repositoryName;
    private int totalFiles;
    private int javaFiles;
    private int javascriptFiles;
    private int otherFiles;

    public RepositoryStatistics(
            Long repositoryId,
            String repositoryName,
            int totalFiles,
            int javaFiles,
            int javascriptFiles,
            int otherFiles) {

        this.repositoryId = repositoryId;
        this.repositoryName = repositoryName;
        this.totalFiles = totalFiles;
        this.javaFiles = javaFiles;
        this.javascriptFiles = javascriptFiles;
        this.otherFiles = otherFiles;
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

    public int getOtherFiles() {
        return otherFiles;
    }
}