class UBNeck(nn.Module):
    def __init__(self, h, w, in_channels, out_channels, p=0.01):
        
        super().__init__()
        
        # Define class variables
        self.in_channels = in_channels
        self.out_channels = out_channels
        self.h = h
        self.w = w
        
        self.unpool = nn.MaxUnpool2d(kernel_size = 2,
                                        stride = 2)
        
        self.main_conv = nn.Conv2d(in_channels = self.in_channels,
                                           out_channels = self.out_channels,
                                           kernel_size = 1)
        
        self.dropout = nn.Dropout2d(p=p)
        
        self.convt1 = nn.ConvTranspose2d(in_channels = self.in_channels,
                               out_channels = self.out_channels,
                               kernel_size = 1,
                               padding = 0,
                               bias = False)
        
        self.prelu1 = nn.PReLU()
        
        self.convt2 = nn.ConvTranspose2d(in_channels = self.out_channels,
                                  out_channels = self.out_channels,
                                  kernel_size = 3,
                                  stride = 2,
                                  padding = 1,
                                  bias = True)
        
        self.prelu2 = nn.PReLU()
        
        self.convt3 = nn.ConvTranspose2d(in_channels = self.out_channels,
                                  out_channels = self.out_channels,
                                  kernel_size = 1,
                                  padding = 0,
                                  bias = False)
        
        self.prelu3 = nn.PReLU()
        
        self.batchnorm = nn.BatchNorm2d(self.out_channels)
        
    def forward(self, x, indices):
        x_copy = x.clone()
        
        # Side Branch
        x = self.convt1(x)
        x = self.batchnorm(x)
        x = self.prelu1(x)
        
        x = self.convt2(x)
        x = self.batchnorm(x)
        x = self.prelu2(x)
        
        x = self.convt3(x)
        x = self.batchnorm(x)
        
        x = self.dropout(x)
        
        # Main Branch
        
        x_copy = self.unpool(x_copy, indices)
        x_copy = self.main_conv(x_copy)
        
        # Concat
        
        x = x + x_copy
        x = self.prelu3(x)
        
        return x
