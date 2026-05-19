package com.ruoyi.dk.quant.domain;

import org.apache.commons.lang3.builder.ToStringBuilder;
import org.apache.commons.lang3.builder.ToStringStyle;
import com.ruoyi.common.annotation.Excel;
import com.ruoyi.common.core.domain.BaseEntity;

/**
 * 策略描述对象 strategy_des
 * 
 * @author ruoyi
 * @date 2025-03-31
 */
public class StrategyDes extends BaseEntity
{
    private static final long serialVersionUID = 1L;

    /** 自增id */
    private Long id;

    /** 策略id */
    @Excel(name = "策略id")
    private Long strategyId;

    /** 详情描述 */
    @Excel(name = "详情描述")
    private String strategyDescription;

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
    public void setStrategyDescription(String strategyDescription) 
    {
        this.strategyDescription = strategyDescription;
    }

    public String getStrategyDescription() 
    {
        return strategyDescription;
    }

    @Override
    public String toString() {
        return new ToStringBuilder(this,ToStringStyle.MULTI_LINE_STYLE)
            .append("id", getId())
            .append("strategyId", getStrategyId())
            .append("strategyDescription", getStrategyDescription())
            .toString();
    }
}
