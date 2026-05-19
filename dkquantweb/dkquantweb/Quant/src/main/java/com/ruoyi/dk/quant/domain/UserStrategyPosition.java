package com.ruoyi.dk.quant.domain;

import io.swagger.annotations.ApiModel;
import io.swagger.annotations.ApiModelProperty;
import org.apache.commons.lang3.builder.ToStringBuilder;
import org.apache.commons.lang3.builder.ToStringStyle;
import com.ruoyi.common.annotation.Excel;
import com.ruoyi.common.core.domain.BaseEntity;

/**
 * 策略仓位对象 user_strategy_position
 * 
 * @author ruoyi
 * @date 2025-02-27
 */
@ApiModel(description = "策略仓位信息")
public class UserStrategyPosition extends BaseEntity
{
    private static final long serialVersionUID = 1L;

    /** id */
    @ApiModelProperty("数据库id")
    private Long id;

    /** 策略id */
    @ApiModelProperty("策略id")
    @Excel(name = "策略id")
    private Long strategyId;

    /** 交易对 */
    @ApiModelProperty("交易对")
    @Excel(name = "交易对")
    private String symbol;

    /** 交易对 */
    @ApiModelProperty("杠杆倍数")
    @Excel(name = "杠杆倍数")
    private String lever;

    /** 数量 */
    @ApiModelProperty("数量")
    @Excel(name = "数量")
    private String sz;

    /** 开仓价格 */
    @ApiModelProperty("开仓价格")
    @Excel(name = "开仓价格")
    private String entryPrice;

    /** 止盈价格 */
    @ApiModelProperty("止盈价格")
    @Excel(name = "止盈价格")
    private String tp;

    /** 止损价格 */
    @ApiModelProperty("止损价格")
    @Excel(name = "止损价格")
    private String sl;

    public void setId(Long id) 
    {
        this.id = id;
    }

    public Long getId() 
    {
        return id;
    }
    public void setStrategyId(Long strategyId) 
    {
        this.strategyId = strategyId;
    }

    public Long getStrategyId() 
    {
        return strategyId;
    }
    public void setSymbol(String symbol) 
    {
        this.symbol = symbol;
    }

    public String getSymbol() 
    {
        return symbol;
    }

    public void setLever(String lever) {this.lever = lever;}

    public String getLever(){return lever;}
    public void setSz(String sz) 
    {
        this.sz = sz;
    }

    public String getSz() 
    {
        return sz;
    }
    public void setEntryPrice(String entryPrice) 
    {
        this.entryPrice = entryPrice;
    }

    public String getEntryPrice() 
    {
        return entryPrice;
    }
    public void setTp(String tp) 
    {
        this.tp = tp;
    }

    public String getTp() 
    {
        return tp;
    }
    public void setSl(String sl) 
    {
        this.sl = sl;
    }

    public String getSl() 
    {
        return sl;
    }

    @Override
    public String toString() {
        return new ToStringBuilder(this,ToStringStyle.MULTI_LINE_STYLE)
            .append("id", getId())
            .append("strategyId", getStrategyId())
            .append("symbol", getSymbol())
            .append("sz", getSz())
            .append("entryPrice", getEntryPrice())
            .append("tp", getTp())
            .append("sl", getSl())
            .append("createTime", getCreateTime())
            .toString();
    }
}
