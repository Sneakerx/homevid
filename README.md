# homevid
Improve old home videos (PAL)

This video processing suite comprises three components that are tailored to old VHS film:
1. Test data generator
2. Processing library
3. Performance assessment

## Description
### Test Data Generator
For estimating the processing capabilities by quality metrics a simultor of VHS quality is needed. High quality video serves as "perfect input" and is degraded by processing filters to generate output in VHS-look. 

#### Camera
The camera itself is the first element that samples the scene. Typical features in this module are spatial motion, unstable gain and defocus. The signal output in this case is PAL.

#### VHS
The analogue signal is limited in bandwidth. The luminance signal is limited to 3 MHz and written to tape in frequency modulation, which is more robust towards noise. Chroma is limited to 400-500 kHz and amplitude modulated, which produces noisy colour. As mitigation several lines are averaged, which reduces vertical resolution.

#### Digitizer
[VHS](https://en.wikipedia.org/wiki/VHS) needs to be replayed and captured to a computer. A typical error during replay is the limited precision to detect the start of horizontal lines. The ADC also introduces compression loss. 

### Processing Library
The processing tries to revert the degradation and thus enhance quality. 

### Performance Assessment
The performance is measured based on objective metrics. Ultimately, the system shall be optimized for a human observer, so the metrics need to be carefully selected. The initial quality can be measured after the test data generator. The output quality after the processing library.

## Getting Started
These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Prerequisites
TBW

### Installing
A step by step series of examples that tell you how to get a development environment running.
TBW

## Running the tests
TBW

## Deployment
TBW

## Built With
TBW

## Contributing
TBW

## Versioning
[SemVer](http://semver.org/) is used for versioning. For the versions available, see the [tags on this repository](https://github.com/Sneakerx/homevid/tags). 

## Authors
* **Marc Bernau** - *Initial work*

## License
TBW
