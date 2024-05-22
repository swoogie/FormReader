# Form Reader

A webapp that detects input fields from a scanned paper form

## Recommended IDE Setup

[VSCode](https://code.visualstudio.com/) + [Volar](https://marketplace.visualstudio.com/items?itemName=Vue.volar) (and disable Vetur) + [TypeScript Vue Plugin (Volar)](https://marketplace.visualstudio.com/items?itemName=Vue.vscode-typescript-vue-plugin).

## Project Requirements

1. [Python 3.11.8](https://www.python.org/downloads/release/python-3118/)
2. [Tesseract](https://tesseract-ocr.github.io/)
3. [Node 20](https://nodejs.org/en)
4. (Optional) Podman or Docker

## Project Setup for Local Development

1. `cd` to project root directory
2. Create and activate Python 3.11 virtual environment
    1) Create `python3 -m venv .venv`
    2) Activate `. .venv/bin/activate`
3. Install project requirements `pip install -r requirements.txt`
4. Install node packages `npm i`
5. Build assets with `npm run build` or, for hot-reload, `npm run watch`
6. Run the application with `python server/app.py`
7. (Optional) Run inside a Docker container
   1) `Ctrl-C` to close locally running server
   2) `(podman/docker) build -t <image_name> .`
   3) `(podman/docker) run -p <localhost_port>:8080 <image_name/image_hash>`

## Node Scripts for [Vite](https://vitejs.dev/)

Below you will find different node scripts you can use to interact with Vite

### Build and Hot-Reload for Development together with [Flask](https://flask.palletsprojects.com/en/3.0.x/)

```sh
npm run watch
```

### Compile and Hot-Reload for Development

```sh
npm run dev
```

### Type-Check, Compile and Minify for Production

```sh
npm run build
```

### Lint with [ESLint](https://eslint.org/)

```sh
npm run lint
```
