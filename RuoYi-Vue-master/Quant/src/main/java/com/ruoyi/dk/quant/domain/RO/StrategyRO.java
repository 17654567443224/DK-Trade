package com.ruoyi.dk.quant.domain.RO;

import com.ruoyi.common.annotation.Excel;
import io.swagger.annotations.ApiModelProperty;
import lombok.Data;

@Data
public class StrategyRO {
    /** 策略id */
    @ApiModelProperty("策略id")
    private Long id;

    /** 策略名称 */
    @ApiModelProperty("策略名称")
    @Excel(name = "策略名称")
    private String strategyName;

    /** 归属(用户id) */
    @ApiModelProperty("归属(用户id)")
    @Excel(name = "归属")
    private Long owner;

    /** 本金 */
    @ApiModelProperty("本金")
    @Excel(name = "本金")
    private Long accountId;

    /** 杠杆 */
    @ApiModelProperty("杠杆")
    @Excel(name = "杠杆")
    private String lever;

    /** 最多持仓 */
    @ApiModelProperty("最多持仓")
    @Excel(name = "最多持仓")
    private Long maxPosition;

    /** 参数 */
    @ApiModelProperty("参数")
    @Excel(name = "参数")
    private Long argsId;
}
