package com.ruoyi.dk.quant.domain;

import org.apache.commons.lang3.builder.ToStringBuilder;
import org.apache.commons.lang3.builder.ToStringStyle;
import com.ruoyi.common.annotation.Excel;
import com.ruoyi.common.core.domain.BaseEntity;

import java.util.Map;

/**
 * 选股策略模板对象 symbol_selection_template
 * 
 * @author ruoyi
 * @date 2025-03-18
 */
public class SymbolSelectionTemplate extends BaseEntity
{
    private static final long serialVersionUID = 1L;

    /** id */
    private Long id;

    /** $column.columnComment */
    @Excel(name = "${comment}", readConverterExp = "$column.readConverterExp()")
    private String fileName;

    /** $column.columnComment */
    @Excel(name = "${comment}", readConverterExp = "$column.readConverterExp()")
    private String className;

    /** $column.columnComment */
    @Excel(name = "${comment}", readConverterExp = "$column.readConverterExp()")
    private String funName;

    /** $column.columnComment */
    @Excel(name = "${comment}", readConverterExp = "$column.readConverterExp()")
    private Map<String, Object> classArgs;

    /** $column.columnComment */
    @Excel(name = "${comment}", readConverterExp = "$column.readConverterExp()")
    private Map<String, Object> funArgs;

    /** $column.columnComment */
    @Excel(name = "${comment}", readConverterExp = "$column.readConverterExp()")
    private Map<String, Object> classArgsDes;

    /** $column.columnComment */
    @Excel(name = "${comment}", readConverterExp = "$column.readConverterExp()")
    private Map<String, Object> funArgsDes;

    /** $column.columnComment */
    @Excel(name = "${comment}", readConverterExp = "$column.readConverterExp()")
    private String cnClassName;

    /** $column.columnComment */
    @Excel(name = "${comment}", readConverterExp = "$column.readConverterExp()")
    private String cnFunName;

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
    public void setFileName(String fileName) 
    {
        this.fileName = fileName;
    }

    public String getFileName() 
    {
        return fileName;
    }
    public void setClassName(String className) 
    {
        this.className = className;
    }

    public String getClassName() 
    {
        return className;
    }
    public void setFunName(String funName) 
    {
        this.funName = funName;
    }

    public String getFunName() 
    {
        return funName;
    }
    public void setClassArgs(Map<String, Object> classArgs)
    {
        this.classArgs = classArgs;
    }

    public Map<String, Object> getClassArgs()
    {
        return classArgs;
    }
    public void setFunArgs(Map<String, Object> funArgs)
    {
        this.funArgs = funArgs;
    }

    public Map<String, Object> getFunArgs()
    {
        return funArgs;
    }
    public void setClassArgsDes(Map<String, Object> classArgsDes)
    {
        this.classArgsDes = classArgsDes;
    }

    public Map<String, Object> getClassArgsDes()
    {
        return classArgsDes;
    }
    public void setFunArgsDes(Map<String, Object> funArgsDes)
    {
        this.funArgsDes = funArgsDes;
    }

    public Map<String, Object> getFunArgsDes()
    {
        return funArgsDes;
    }
    public void setCnClassName(String cnClassName) 
    {
        this.cnClassName = cnClassName;
    }

    public String getCnClassName() 
    {
        return cnClassName;
    }
    public void setCnFunName(String cnFunName) 
    {
        this.cnFunName = cnFunName;
    }

    public String getCnFunName() 
    {
        return cnFunName;
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
            .append("fileName", getFileName())
            .append("className", getClassName())
            .append("funName", getFunName())
            .append("classArgs", getClassArgs())
            .append("funArgs", getFunArgs())
            .append("classArgsDes", getClassArgsDes())
            .append("funArgsDes", getFunArgsDes())
            .append("cnClassName", getCnClassName())
            .append("cnFunName", getCnFunName())
                .append("owner", getOwner())
            .toString();
    }
}
