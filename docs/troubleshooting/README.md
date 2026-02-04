---
title: Troubleshooting Guide
description: Common issues and solutions for the Docling Workshop
logo: images/DoclingDuck.png
---

# Troubleshooting Guide

This guide covers common issues you might encounter during the workshop and their solutions.

## Installation Issues

### Python Version Errors

**Problem**: Assertion error about Python version

```
AssertionError: Use Python 3.10, 3.11, 3.12, or 3.13 to run this notebook.
```

**Solution**:

1. Check your Python version:
    ```shell
    python3 --version
    ```

2. If using an older version, install a supported version:
    - macOS: `brew install python@3.12`
    - Ubuntu: `sudo apt install python3.12`
    - Windows: Download from [python.org](https://www.python.org/downloads/)

3. Create a new virtual environment with the correct version:
    ```shell
    python3.12 -m venv venv
    source venv/bin/activate
    ```

### Dependency Installation Failures

**Problem**: `pip install` fails with compilation errors

**Solution**:

1. Ensure you have build tools installed:
    - macOS: `xcode-select --install`
    - Ubuntu: `sudo apt install build-essential`
    - Windows: Install [Visual Studio Build Tools](https://visualstudio.microsoft.com/visual-cpp-build-tools/)

2. Try using `uv` for faster, more reliable installs:
    ```shell
    pip install uv
    uv pip install docling
    ```

### Memory Errors During Installation

**Problem**: Installation runs out of memory

**Solution**:

1. Close other applications to free memory
2. Install packages one at a time instead of all at once
3. Use `--no-cache-dir` flag:
    ```shell
    pip install --no-cache-dir docling
    ```

## Model Loading Issues

### VLM Models Won't Load

**Problem**: Error loading SmolDocling or Granite Vision models

**Solution**:

1. Check available memory - VLM models require 4-8 GB RAM
2. Try a smaller model first
3. For Apple Silicon, ensure MLX backend is used:
    ```python
    from docling.datamodel.pipeline_options import smoldocling_vlm_mlx_conversion_options
    ```

### Ollama/LM Studio Connection Errors

**Problem**: Cannot connect to local model server

**Solution**:

1. Verify the server is running:
    ```shell
    curl http://localhost:11434/api/tags  # Ollama
    curl http://localhost:1234/v1/models  # LM Studio
    ```

2. Check the port is correct in your code
3. Ensure no firewall is blocking localhost connections

## Document Processing Issues

### PDF Conversion Fails

**Problem**: Error converting certain PDFs

**Solution**:

1. Try enabling OCR for scanned documents:
    ```python
    PdfPipelineOptions(do_ocr=True)
    ```

2. Check if the PDF is password-protected
3. Try converting a simpler PDF first to verify setup

### Out of Memory During Conversion

**Problem**: Kernel dies or out of memory error

**Solution**:

1. Process fewer pages at a time
2. Reduce image resolution:
    ```python
    PdfPipelineOptions(images_scale=1.0)  # Instead of 2.0
    ```

3. Disable features you don't need:
    ```python
    PdfPipelineOptions(
        generate_page_images=False,
        generate_picture_images=False,
    )
    ```

### Slow Document Processing

**Problem**: Conversion takes too long

**Solution**:

1. Disable OCR if not needed (`do_ocr=False`)
2. Reduce image quality for faster processing
3. Use a GPU if available
4. For large documents, save JSON output and reuse:
    ```python
    doc.save_as_json("document.json")
    # Later:
    doc = DoclingDocument.load_from_json("document.json")
    ```

## Replicate API Issues

### Rate Limiting

**Problem**: "Too many requests" error from Replicate

**Solution**:

1. Add delays between requests
2. Use local inference instead (LM Studio or Ollama)
3. Contact Replicate for higher rate limits

### API Token Issues

**Problem**: Authentication errors

**Solution**:

1. Verify your token is set:
    ```shell
    echo $REPLICATE_API_TOKEN
    ```

2. Regenerate your token at [replicate.com/account/api-tokens](https://replicate.com/account/api-tokens)

3. For Colab, check the Secrets tab has the correct value

## Vector Database Issues

### Milvus Lite Errors

**Problem**: Database connection or storage errors

**Solution**:

1. Use a fresh database file:
    ```python
    import tempfile
    db_file = tempfile.NamedTemporaryFile(suffix=".db", delete=False).name
    ```

2. Ensure you have write permissions to the directory
3. Check disk space is available

## Jupyter Notebook Issues

### Kernel Dies Unexpectedly

**Problem**: Jupyter kernel crashes during execution

**Solution**:

1. Check system memory usage
2. Run memory-intensive cells one at a time
3. Restart the kernel and run cells in order
4. Consider using Google Colab for more resources

### Widgets Not Displaying

**Problem**: ipywidgets not showing in notebook

**Solution**:

1. Install the widget extension:
    ```shell
    pip install ipywidgets
    jupyter nbextension enable --py widgetsnbextension
    ```

2. Restart Jupyter after installation

## Getting Help

If you encounter an issue not covered here:

1. Check the [Docling GitHub Issues](https://github.com/docling-project/docling/issues)
2. Search the [Docling Discussions](https://github.com/docling-project/docling/discussions)
3. Open a new issue with:
    - Your Python version
    - Your operating system
    - The complete error message
    - Steps to reproduce the issue
