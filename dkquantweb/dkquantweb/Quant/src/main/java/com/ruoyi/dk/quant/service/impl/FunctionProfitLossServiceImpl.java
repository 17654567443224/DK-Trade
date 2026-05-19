package com.ruoyi.dk.quant.service.impl;

import java.util.List;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import com.ruoyi.dk.quant.mapper.FunctionProfitLossMapper;
import com.ruoyi.dk.quant.domain.FunctionProfitLoss;
import com.ruoyi.dk.quant.service.IFunctionProfitLossService;

/**
 * 止盈止损方法Service业务层处理
 * 
 * @author ruoyi
 * @date 2025-02-27
 */
@Service
public class FunctionProfitLossServiceImpl implements IFunctionProfitLossService 
{
    @Autowired
    private FunctionProfitLossMapper functionProfitLossMapper;

    /**
     * 查询止盈止损方法
     * 
     * @param id 止盈止损方法主键
     * @return 止盈止损方法
     */
    @Override
    public FunctionProfitLoss selectFunctionProfitLossById(Long id)
    {
        return functionProfitLossMapper.selectFunctionProfitLossById(id);
    }

    /**
     * 查询止盈止损方法列表
     * 
     * @param functionProfitLoss 止盈止损方法
     * @return 止盈止损方法
     */
    @Override
    public List<FunctionProfitLoss> selectFunctionProfitLossList(FunctionProfitLoss functionProfitLoss)
    {
        return functionProfitLossMapper.selectFunctionProfitLossList(functionProfitLoss);
    }

    /**
     * 新增止盈止损方法
     * 
     * @param functionProfitLoss 止盈止损方法
     * @return 结果
     */
    @Override
    public int insertFunctionProfitLoss(FunctionProfitLoss functionProfitLoss)
    {
        return functionProfitLossMapper.insertFunctionProfitLoss(functionProfitLoss);
    }

    /**
     * 修改止盈止损方法
     * 
     * @param functionProfitLoss 止盈止损方法
     * @return 结果
     */
    @Override
    public int updateFunctionProfitLoss(FunctionProfitLoss functionProfitLoss)
    {
        return functionProfitLossMapper.updateFunctionProfitLoss(functionProfitLoss);
    }

    /**
     * 批量删除止盈止损方法
     * 
     * @param ids 需要删除的止盈止损方法主键
     * @return 结果
     */
    @Override
    public int deleteFunctionProfitLossByIds(Long[] ids)
    {
        return functionProfitLossMapper.deleteFunctionProfitLossByIds(ids);
    }

    /**
     * 删除止盈止损方法信息
     * 
     * @param id 止盈止损方法主键
     * @return 结果
     */
    @Override
    public int deleteFunctionProfitLossById(Long id)
    {
        return functionProfitLossMapper.deleteFunctionProfitLossById(id);
    }
}
