# vsdkx-addon-box-filtering

*No addon config required*

Computes **Inter Quartile Range** on bounding box areas after model inference 
and filters out boxes that fall in upper bound

```
IQR = Quartile3 – Quartile1 (Inter Quartile Range)
Lower Bound: (Quartile1 - 1.5 * IQR)
Upper Bound: (Quartile3 + 1.5 * IQR)
```