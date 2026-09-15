package com.repolens.backend.model;

import jakarta.persistence.CascadeType;
import jakarta.persistence.Entity;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.GenerationType;
import jakarta.persistence.Id;
import jakarta.persistence.OneToMany;
import jakarta.persistence.FetchType;

import java.util.ArrayList;
import java.util.List;

@Entity
public class Repository {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    private String name;

    private String url;

 @OneToMany(
        mappedBy = "repository",
        cascade = CascadeType.ALL,
        orphanRemoval = true,
        fetch = FetchType.EAGER
)
private List<RepositoryFile> files = new ArrayList<>();

    public Repository() {
    }

    public Repository(String name, String url) {
        this.name = name;
        this.url = url;
    }

    public Long getId() {
        return id;
    }

    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }

    public String getUrl() {
        return url;
    }

    public void setUrl(String url) {
        this.url = url;
    }

    public List<RepositoryFile> getFiles() {
        return files;
    }

    public void setFiles(List<RepositoryFile> files) {
        this.files = files;
    }

    public void addFile(RepositoryFile file) {
        files.add(file);
        file.setRepository(this);
    }

    public void removeFile(RepositoryFile file) {
        files.remove(file);
        file.setRepository(null);
    }
}