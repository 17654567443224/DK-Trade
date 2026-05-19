package com.ruoyi.dk.quant.mapper;

import java.util.List;
import com.ruoyi.dk.quant.domain.FunctionProfitLoss;

/**
 * 止盈止损方法Mapper接口
 * 
 * @author ruoyi
 * @date 2025-02-27
 */
public interface FunctionProfitLossMapper 
{
    /**
     * 查询止盈止损方法
     * 
     * @param id 止盈止损方法主键
     * @return 止盈止损方法
     */
    public FunctionProfitLoss selectFunctionProfitLossById(Long id);

    /**
     * 查询止盈止损方法列表
     * 
     * @param functionProfitLoss 止盈止损方法
     * @return 止盈止损方法集合
     */
    public List<FunctionProfitLoss> selectFunctionProfitLossList(FunctionProfitLoss functionProfitLoss);

    /**
     * 新增止盈止损方法
     * 
     * @param functionProfitLoss 止盈止损方法
     * @return 结果
     */
    public int insertFunctionProfitLoss(FunctionProfitLoss functionProfitLoss);

    /**
     * 修改止盈止损方法
     * 
     * @param functionProfitLoss 止盈止损方法
     * @return 结果
     */
    public int updateFunctionProfitLoss(FunctionProfitLoss functionProfitLoss);

    /**
     * 删除止盈止损方法
     * 
     * @param id 止盈止损方法主键
     * @return 结果
     */
    public int deleteFunctionProfitLossById(Long id);

    /**
     * 批量删除止盈止损方法
     * 
     * @param ids 需要删除的数据主键集合
     * @return 结果
     */
    public int deleteFunctionProfitLossByIds(Long[] ids);
}
