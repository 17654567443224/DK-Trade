package com.ruoyi.dk.quant.service;

import java.util.List;
import com.ruoyi.dk.quant.domain.FunctionOpenPosition;

/**
 * 开仓方法Service接口
 * 
 * @author ruoyi
 * @date 2025-02-27
 */
public interface IFunctionOpenPositionService 
{
    /**
     * 查询开仓方法
     * 
     * @param id 开仓方法主键
     * @return 开仓方法
     */
    public FunctionOpenPosition selectFunctionOpenPositionById(Long id);

    /**
     * 查询开仓方法列表
     * 
     * @param functionOpenPosition 开仓方法
     * @return 开仓方法集合
     */
    public List<FunctionOpenPosition> selectFunctionOpenPositionList(FunctionOpenPosition functionOpenPosition);

    /**
     * 新增开仓方法
     * 
     * @param functionOpenPosition 开仓方法
     * @return 结果
     */
    public int insertFunctionOpenPosition(FunctionOpenPosition functionOpenPosition);

    /**
     * 修改开仓方法
     * 
     * @param functionOpenPosition 开仓方法
     * @return 结果
     */
    public int updateFunctionOpenPosition(FunctionOpenPosition functionOpenPosition);

    /**
     * 批量删除开仓方法
     * 
     * @param ids 需要删除的开仓方法主键集合
     * @return 结果
     */
    public int deleteFunctionOpenPositionByIds(Long[] ids);

    /**
     * 删除开仓方法信息
     * 
     * @param id 开仓方法主键
     * @return 结果
     */
    public int deleteFunctionOpenPositionById(Long id);
}
