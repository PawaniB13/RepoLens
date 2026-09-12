package com.repolens.backend.model;

import jakarta.persistence.Entity;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.GenerationType;
import jakarta.persistence.Id;

@Entity
public class RepositoryAnalysis {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    private Long repositoryId;
    private String repositoryName;

    private int totalFiles;
    private int javaFiles;
    private int javascriptFiles;

    private String language;
    private int stars;
    private int forks;
    private int openIssues;
    private String defaultBranch;

    public RepositoryAnalysis() {
    }

    public RepositoryAnalysis(
            Long repositoryId,
            String repositoryName,
            int totalFiles,
            int javaFiles,
            int javascriptFiles
    ) {
        this.repositoryId = repositoryId;
        this.repositoryName = repositoryName;
        this.totalFiles = totalFiles;
        this.javaFiles = javaFiles;
        this.javascriptFiles = javascriptFiles;
    }

    public Long getId() {
        return id;
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

    public String getLanguage() {
        return language;
    }

    public void setLanguage(String language) {
        this.language = language;
    }

    public int getStars() {
        return stars;
    }

    public void setStars(int stars) {
        this.stars = stars;
    }

    public int getForks() {
        return forks;
    }

    public void setForks(int forks) {
        this.forks = forks;
    }

    public int getOpenIssues() {
        return openIssues;
    }

    public void setOpenIssues(int openIssues) {
        this.openIssues = openIssues;
    }

    public String getDefaultBranch() {
        return defaultBranch;
    }

    public void setDefaultBranch(String defaultBranch) {
        this.defaultBranch = defaultBranch;
    }
}
