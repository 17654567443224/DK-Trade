package com.ruoyi.dk.quant.client.PO;

import com.ruoyi.dk.quant.domain.UserStrategyAccount;
import com.ruoyi.dk.quant.domain.UserStrategyArgs;
import lombok.Data;

@Data
public class AddStrategy {
    private Long id;
    private String action;
    private Long owner;
    private String account;
    private String lever;
    private Long maxPosition;
    private String args;
    private String funDict;
}
