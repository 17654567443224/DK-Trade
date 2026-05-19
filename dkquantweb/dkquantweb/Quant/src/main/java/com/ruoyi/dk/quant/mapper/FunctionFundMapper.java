package com.ruoyi.dk.quant.mapper;

import java.util.List;
import com.ruoyi.dk.quant.domain.FunctionFund;

/**
 * 资金方法Mapper接口
 * 
 * @author ruoyi
 * @date 2025-02-27
 */
public interface FunctionFundMapper 
{
    /**
     * 查询资金方法
     * 
     * @param id 资金方法主键
     * @return 资金方法
     */
    public FunctionFund selectFunctionFundById(Long id);

    /**
     * 查询资金方法列表
     * 
     * @param functionFund 资金方法
     * @return 资金方法集合
     */
    public List<FunctionFund> selectFunctionFundList(FunctionFund functionFund);

    /**
     * 新增资金方法
     * 
     * @param functionFund 资金方法
     * @return 结果
     */
    public int insertFunctionFund(FunctionFund functionFund);

    /**
     * 修改资金方法
     * 
     * @param functionFund 资金方法
     * @return 结果
     */
    public int updateFunctionFund(FunctionFund functionFund);

    /**
     * 删除资金方法
     * 
     * @param id 资金方法主键
     * @return 结果
     */
    public int deleteFunctionFundById(Long id);

    /**
     * 批量删除资金方法
     * 
     * @param ids 需要删除的数据主键集合
     * @return 结果
     */
    public int deleteFunctionFundByIds(Long[] ids);
}
