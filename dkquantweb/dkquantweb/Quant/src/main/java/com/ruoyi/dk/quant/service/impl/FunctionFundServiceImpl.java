package com.ruoyi.dk.quant.service.impl;

import java.util.List;

import com.fasterxml.jackson.databind.ObjectMapper;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import com.ruoyi.dk.quant.mapper.FunctionFundMapper;
import com.ruoyi.dk.quant.domain.FunctionFund;
import com.ruoyi.dk.quant.service.IFunctionFundService;

/**
 * 资金方法Service业务层处理
 * 
 * @author ruoyi
 * @date 2025-02-27
 */
@Service
public class FunctionFundServiceImpl implements IFunctionFundService 
{
    @Autowired
    private FunctionFundMapper functionFundMapper;

    /**
     * 查询资金方法
     * 
     * @param id 资金方法主键
     * @return 资金方法
     */
    @Override
    public FunctionFund selectFunctionFundById(Long id)
    {
        return functionFundMapper.selectFunctionFundById(id);
    }

    /**
     * 查询资金方法列表
     * 
     * @param functionFund 资金方法
     * @return 资金方法
     */
    @Override
    public List<FunctionFund> selectFunctionFundList(FunctionFund functionFund)
    {
        return functionFundMapper.selectFunctionFundList(functionFund);
    }

    /**
     * 新增资金方法
     * 
     * @param functionFund 资金方法
     * @return 结果
     */
    @Override
    public int insertFunctionFund(FunctionFund functionFund)
    {
        return functionFundMapper.insertFunctionFund(functionFund);
    }

    /**
     * 修改资金方法
     * 
     * @param functionFund 资金方法
     * @return 结果
     */
    @Override
    public int updateFunctionFund(FunctionFund functionFund)
    {
        return functionFundMapper.updateFunctionFund(functionFund);
    }

    /**
     * 批量删除资金方法
     * 
     * @param ids 需要删除的资金方法主键
     * @return 结果
     */
    @Override
    public int deleteFunctionFundByIds(Long[] ids)
    {
        return functionFundMapper.deleteFunctionFundByIds(ids);
    }

    /**
     * 删除资金方法信息
     * 
     * @param id 资金方法主键
     * @return 结果
     */
    @Override
    public int deleteFunctionFundById(Long id)
    {
        return functionFundMapper.deleteFunctionFundById(id);
    }
}
