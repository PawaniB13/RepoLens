package com.repolens.backend.dto;

public class GitHubImportRequest {

    private String repo;

    public GitHubImportRequest() {
    }

    public String getRepo() {
        return repo;
    }

    public void setRepo(String repo) {
        this.repo = repo;
    }
}