package com.ruoyi.dk.quant.client.PRO;

import lombok.Data;

@Data
public class BaseResponse {
    private Long code;
    private String msg;
    private Object data;
}
