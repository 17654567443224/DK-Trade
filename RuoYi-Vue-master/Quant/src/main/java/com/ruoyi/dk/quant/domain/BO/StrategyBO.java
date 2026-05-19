package com.ruoyi.dk.quant.domain.BO;

import com.fasterxml.jackson.annotation.JsonCreator;
import lombok.Data;

import java.util.HashMap;

@Data
public class StrategyBO {
    /**
     * 策略ID
     */
    private Long id;

    /**
     * 归属
     */
    private Long owner = 1L;

    /**
     * 本金
     */
    private Long accountId;

    // 添加此构造方法，支持从数字反序列化
    @JsonCreator
    public StrategyBO(Long id) {
        this.id = id;
        this.owner = 1L; // 默认值
    }
    // 必须保留无参构造方法
    public StrategyBO() {}
}
