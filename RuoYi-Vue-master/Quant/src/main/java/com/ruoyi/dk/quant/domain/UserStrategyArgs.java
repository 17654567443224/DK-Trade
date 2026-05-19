package com.ruoyi.dk.quant.domain;

import io.swagger.annotations.ApiModel;
import io.swagger.annotations.ApiModelProperty;
import org.apache.commons.lang3.builder.ToStringBuilder;
import org.apache.commons.lang3.builder.ToStringStyle;
import com.ruoyi.common.annotation.Excel;
import com.ruoyi.common.core.domain.BaseEntity;

/**
 * 策略参数信息对象 user_strategy_args
 * 
 * @author ruoyi
 * @date 2025-02-25
 */
@ApiModel(description = "策略参数信息")
public class UserStrategyArgs extends BaseEntity
{
    private static final long serialVersionUID = 1L;

    /** id */
    @ApiModelProperty("数据库id")
    private Long id;

    /** 私有路径 */
    @ApiModelProperty("私有路径")
    private Long pv;

    /** 选股策略 */
    @ApiModelProperty("选股策略")
    private Long symbolSelection;

    /** 开仓策略 */
    @ApiModelProperty("开仓策略")
    private Long openPosition;

    /** 止盈止损策略 */
    @ApiModelProperty("止盈止损策略")
    private Long profitLoss;

    /** 资金策略 */
    @ApiModelProperty("资金策略")
    private Long fund;

    public void setId(Long id) 
    {
        this.id = id;
    }
    public Long getId() 
    {
        return id;
    }
    public void setPv(Long pv)
    {
        this.pv = pv;
    }
    public Long getPv()
    {
        return pv;
    }
    public void setSymbolSelection(Long symbolSelection)
    {
        this.symbolSelection = symbolSelection;
    }
    public Long getSymbolSelection()
    {
        return symbolSelection;
    }
    public void setOpenPosition(Long openPosition)
    {
        this.openPosition = openPosition;
    }
    public Long getOpenPosition()
    {
        return openPosition;
    }
    public void setProfitLoss(Long profitLoss)
    {
        this.profitLoss = profitLoss;
    }
    public Long getProfitLoss()
    {
        return profitLoss;
    }
    public void setFund(Long fund)
    {
        this.fund = fund;
    }
    public Long getFund()
    {
        return fund;
    }


    @Override
    public String toString() {
        return new ToStringBuilder(this,ToStringStyle.MULTI_LINE_STYLE)
            .append("id", getId())
            .append("pv", getPv())
            .append("symbolSelection", getSymbolSelection())
            .append("openPosition", getOpenPosition())
            .append("profitLoss", getProfitLoss())
            .append("fund", getFund())
            .toString();
    }
}
