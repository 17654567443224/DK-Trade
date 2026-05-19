package com.ruoyi.dk.quant.domain;

import org.apache.commons.lang3.builder.ToStringBuilder;
import org.apache.commons.lang3.builder.ToStringStyle;
import com.ruoyi.common.annotation.Excel;
import com.ruoyi.common.core.domain.BaseEntity;

import java.util.Map;

/**
 * 指标对象 target_methods
 * 
 * @author ruoyi
 * @date 2025-03-18
 */
public class TargetMethods extends BaseEntity
{
    private static final long serialVersionUID = 1L;

    /** $column.columnComment */
    private Long id;

    /** $column.columnComment */
    @Excel(name = "${comment}", readConverterExp = "$column.readConverterExp()")
    private String methodName;

    /** $column.columnComment */
    @Excel(name = "${comment}", readConverterExp = "$column.readConverterExp()")
    private Map<String, Object> parameters;

    /** $column.columnComment */
    @Excel(name = "${comment}", readConverterExp = "$column.readConverterExp()")
    private Map<String, Object> parametersDes;

    /** $column.columnComment */
    @Excel(name = "${comment}", readConverterExp = "$column.readConverterExp()")
    private Long owner;

    public void setId(Long id) 
    {
        this.id = id;
    }

    public Long getId() 
    {
        return id;
    }
    public void setMethodName(String methodName) 
    {
        this.methodName = methodName;
    }

    public String getMethodName() 
    {
        return methodName;
    }
    public void setParameters(Map<String, Object> parameters)
    {
        this.parameters = parameters;
    }

    public Map<String, Object> getParameters()
    {
        return parameters;
    }
    public void setParametersDes(Map<String, Object> parametersDes)
    {
        this.parametersDes = parametersDes;
    }

    public Map<String, Object> getParametersDes()
    {
        return parametersDes;
    }
    public void setOwner(Long owner){
        this.owner = owner;
    }
    public Long getOwner(){
        return owner;
    }
    @Override
    public String toString() {
        return new ToStringBuilder(this,ToStringStyle.MULTI_LINE_STYLE)
            .append("id", getId())
            .append("methodName", getMethodName())
            .append("parameters", getParameters())
            .append("parametersDes", getParametersDes())
                .append("owner", getOwner())
            .toString();
    }
}
