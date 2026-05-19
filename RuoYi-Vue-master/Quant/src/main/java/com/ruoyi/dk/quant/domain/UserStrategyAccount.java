package com.ruoyi.dk.quant.domain;

import io.swagger.annotations.ApiModel;
import io.swagger.annotations.ApiModelProperty;
import org.apache.commons.lang3.builder.ToStringBuilder;
import org.apache.commons.lang3.builder.ToStringStyle;
import com.ruoyi.common.annotation.Excel;
import com.ruoyi.common.core.domain.BaseEntity;
import org.springframework.data.annotation.Transient;

/**
 * 策略账户信息对象 user_strategy_account
 * 
 * @author ruoyi
 * @date 2025-02-27
 */
@ApiModel(description = "策略账户信息")
public class UserStrategyAccount extends BaseEntity
{
    private static final long serialVersionUID = 1L;

    /** id */
    @ApiModelProperty("数据库id")
    private Long id;

    /** 资金 */
    @ApiModelProperty("资金")
    @Excel(name = "资金")
    private String balance;

    /** 手续费 */
    @ApiModelProperty("手续费")
    @Excel(name = "手续费")
    private String orderFee;

    /** 仓位数据 */
    @ApiModelProperty("仓位数据")
    @Transient
    private UserStrategyPosition position;

    /** 订单数据 */
    @ApiModelProperty("订单数据")
    @Transient
    private UserStrategyOrders orders;

    public void setId(Long id) 
    {
        this.id = id;
    }

    public Long getId() 
    {
        return id;
    }
    public void setBalance(String balance) 
    {
        this.balance = balance;
    }

    public String getBalance() 
    {
        return balance;
    }
    public void setOrderFee(String orderFee) 
    {
        this.orderFee = orderFee;
    }

    public String getOrderFee() 
    {
        return orderFee;
    }
    public void setPosition(UserStrategyPosition position)
    {
        this.position = position;
    }
    public void setOrders(UserStrategyOrders orders)
    {
        this.orders = orders;
    }

    public UserStrategyOrders getOrders()
    {
        return orders;
    }

    public UserStrategyPosition getPosition()
    {
        return position;
    }
    @Override
    public String toString() {
        return new ToStringBuilder(this,ToStringStyle.MULTI_LINE_STYLE)
            .append("id", getId())
            .append("balance", getBalance())
            .append("orderFee", getOrderFee())
            .toString();
    }
}
