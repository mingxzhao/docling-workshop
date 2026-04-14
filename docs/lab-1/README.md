---
title: Lab 1. Document Conversion with Docling
description: Document Conversion with Docling
logo: images/DoclingDuck.png
notebook: notebooks/Conversion.ipynb
---

# Document Conversion with Docling

The primary purpose of Docling is Document conversion. Docling enables us to convert documents various format into formats that are more useful in AI applications, while preserving document structure.

This lab walks through the different document conversion options Docling offers, as well as some enrichment features. We will also explore the converted documents to examine how Docling stores metadata to preserve document structure.

## Prerequisites

This lab is a [Jupyter notebook](https://jupyter.org/). Please follow the instructions in [pre-work](../pre-work/README.md) to run the lab.

## Lab

[![Document Conversion with Docling Notebook](https://badgen.net/badge/icon/github?icon=github&label=View%20on "View on GitHub")]({{ config.repo_url }}/blob/{{ git.commit }}/{{ notebook }}){:target="_blank"}
[![Document Conversion with Docling Notebook](https://colab.research.google.com/assets/colab-badge.svg "Open In Colab")]({{ extra.colab_url }}/blob/{{ git.commit }}/{{ notebook }}){:target="_blank"}

### Google Colab (Replicate Edition)

If you are running in **Google Colab** and want a streamlined experience using [Replicate](https://replicate.com) for hosted model inference (no local GPU or Ollama required), use this alternate notebook:

[![Colab + Replicate Notebook](https://colab.research.google.com/assets/colab-badge.svg "Open In Colab")]({{ extra.colab_url }}/blob/{{ git.commit }}/notebooks/Conversion_Colab.ipynb){:target="_blank"}

To run the notebook from your command line in Jupyter using the active virtual environment from the [pre-work](../pre-work/README.md#install-jupyter), run:

```shell
jupyter notebook {{ notebook }}
```

The path of the notebook file above is relative to the `docling-workshop` folder from the git clone in the [pre-work](../pre-work/README.md#clone-the-docling-workshop-repository).
