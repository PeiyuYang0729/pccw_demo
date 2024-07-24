Required packages:
- pip3 install selenium
- pip3 install torch
- pip3 install git+https://github.com/openai/CLIP.git
- pip3 install clip-score

How to run script:
- cmd: python3 searchImage.py
- Source image is saving under ./demo, downloaded baidu image is downloaded under folder ./download.
If no folder downloaded, it will be created automatically.

Result:
- Test passed:
    - Picture similar score over 80
    - example:
    Test passed, score:  92.67405700683594
    File path is /Users/peiyu/Documents/pccw/download/demo.png
- Test failed
    - Picture similar score less than 80

Demo screen recording is Screen Recording 2024-07-24 at 13.38.46.mov