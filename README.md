<div align=center><img src="frontend/src/assets/logo.png" alt="logo" width="500"/></div>

# Anime-Paintbrush

A web-based animation coloring tool, capable of reconstructing sketches into colored images in real time. The uploaded sketch would be preprocessed and some hints about color are needed to provide color information, two parts combining to be put into input. The rendered colorized anime characters will be the output. 

This project is developed with `javascript`, `python`, `css`, etc. The front-end development of this project uses `Vue` with `Element-ui` , with the back-end development using `Django`.


## Table of Contents

- [Background](#background)
- [Install](#install)
- [Usage](#usage)
  - [Generator](#generator)
- [Badge](#badge)
- [Example Readmes](#example-readmes)
- [Related Efforts](#related-efforts)
- [Maintainers](#maintainers)
- [Contributing](#contributing)
- [License](#license)

## Background

As a painting enthusiast, I have tried different ways of painting, such as pen sketching, oil painting, watercolor, etc. The most convenient one is pen sketching, where the basic concern is to outline the object. However, for human perception and the situation where the most applications are currently put, color is essential for drawing.

Thus it is meaningful to design a tool that would **automatically assist in generating high quality images by simply entering a sketch with a little color cue**. By learning through generative adversarial networks (GAN), neural networks can learn pretty good drawing skills. This project deploys the trained neural network on the back-end, while the front-end is deployed on a web application, and a user-friendly interface is designed so that users can complete the color rendering of sketches and download them through simple operations on the web page.

The goals for this repository are:

1. Provide efficient coloring tools for drawing practitioners to improve drawing efficiency.
2. Provide non-professionals with the opportunity to draw high-quality manga characters at a low learning cost.
3. Provide a reference for programmers since all the code has  been open sourced.

## Install

The back-end is developed with `python3.7`. Make sure you have an available environment. In your environment, install the required packages.

```sh
pip install -r requirements.txt
```

This project uses [npm](https://npmjs.com). Go check them out if you don't have them locally installed.

```sh
$ npm install --global standard-readme-spec
```

## Usage

This is only a documentation package. You can print out [spec.md](spec.md) to your console:

```sh
$ standard-readme-spec
# Prints out the standard-readme spec
```

### Generator

To use the generator, look at [generator-standard-readme](https://github.com/RichardLitt/generator-standard-readme). There is a global executable to run the generator in that package, aliased as `standard-readme`.

## Badge

If your README is compliant with Standard-Readme and you're on GitHub, it would be great if you could add the badge. This allows people to link back to this Spec, and helps adoption of the README. The badge is **not required**.

[![standard-readme compliant](https://img.shields.io/badge/readme%20style-standard-brightgreen.svg?style=flat-square)](https://github.com/RichardLitt/standard-readme)

To add in Markdown format, use this code:

```
[![standard-readme compliant](https://img.shields.io/badge/readme%20style-standard-brightgreen.svg?style=flat-square)](https://github.com/RichardLitt/standard-readme)
```

## Example Readmes

To see how the specification has been applied, see the [example-readmes](example-readmes/).

## Related Efforts

- [Art of Readme](https://github.com/noffle/art-of-readme) - 💌 Learn the art of writing quality READMEs.
- [open-source-template](https://github.com/davidbgk/open-source-template/) - A README template to encourage open-source contributions.

## Maintainers

[@RichardLitt](https://github.com/RichardLitt).

## Contributing

Feel free to dive in! [Open an issue](https://github.com/RichardLitt/standard-readme/issues/new) or submit PRs.

Standard Readme follows the [Contributor Covenant](http://contributor-covenant.org/version/1/3/0/) Code of Conduct.

### Contributors

This project exists thanks to all the people who contribute. 
<a href="https://github.com/RichardLitt/standard-readme/graphs/contributors"><img src="https://opencollective.com/standard-readme/contributors.svg?width=890&button=false" /></a>


## License

[MIT](LICENSE) © Richard Littauer
