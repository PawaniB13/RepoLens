package com.repolens.backend.dto;

public class GitHubImportRequest {

    private String owner;
    private String repo;

    public GitHubImportRequest() {
    }

    public String getOwner() {
        return owner;
    }

    public void setOwner(String owner) {
        this.owner = owner;
    }

    public String getRepo() {
        return repo;
    }

    public void setRepo(String repo) {
        this.repo = repo;
    }
}
