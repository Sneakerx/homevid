# homevid
Improve old home videos (PAL)

This video processing suite comprises three components that are tailored to old VHS film:
1. Test data generator
2. Processing library
3. Performance assessment

# Test Data Generator
For estimating the processing capabilities by quality metrics a simultor of VHS quality is needed. High quality video serves as "perfect input" and is degraded by processing filters to generate output in VHS-look. 

## Camera
The camera itself is the first element that converts the scene to an analogue representation on internal tape.

## VHS [1]
The analogue signal is compressed by limiting the bandwidth. The luminance signal is limited to 3 MHz and written to tape in frequency modulation, which is more robust towards noise. Chorma is limited to 400-500 kHz and amplitude modulated, which produces noisy colour. As mitigation several lines are averaged, which aldo reduces the vertical resolution.

## Digitizer
VHS needs to be replayed and captured to a computer. A typical error during replay is the limited precision to detect the start of horizontal lines. The ADC also introduces compression loss. 

# Processing Library
The processing tries to revert the degradation and thus enhance quality. 

# Performance Assessment
The performance is measured based on objective metrics. Ultimately, the system shall be optimized for a human observer, so the metrics need to be carefully selected. The initial quality can be measured after the test data generator. The output quality after the processing library.

# References
[1] https://de.wikipedia.org/wiki/Video_Home_System
