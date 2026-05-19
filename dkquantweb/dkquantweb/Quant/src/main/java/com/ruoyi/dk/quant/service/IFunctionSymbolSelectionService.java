package com.ruoyi.dk.quant.service;

import java.util.List;
import com.ruoyi.dk.quant.domain.FunctionSymbolSelection;

/**
 * 选股方法Service接口
 * 
 * @author ruoyi
 * @date 2025-02-27
 */
public interface IFunctionSymbolSelectionService 
{
    /**
     * 查询选股方法
     * 
     * @param id 选股方法主键
     * @return 选股方法
     */
    public FunctionSymbolSelection selectFunctionSymbolSelectionById(Long id);

    /**
     * 查询选股方法列表
     * 
     * @param functionSymbolSelection 选股方法
     * @return 选股方法集合
     */
    public List<FunctionSymbolSelection> selectFunctionSymbolSelectionList(FunctionSymbolSelection functionSymbolSelection);

    /**
     * 新增选股方法
     * 
     * @param functionSymbolSelection 选股方法
     * @return 结果
     */
    public int insertFunctionSymbolSelection(FunctionSymbolSelection functionSymbolSelection);

    /**
     * 修改选股方法
     * 
     * @param functionSymbolSelection 选股方法
     * @return 结果
     */
    public int updateFunctionSymbolSelection(FunctionSymbolSelection functionSymbolSelection);

    /**
     * 批量删除选股方法
     * 
     * @param ids 需要删除的选股方法主键集合
     * @return 结果
     */
    public int deleteFunctionSymbolSelectionByIds(Long[] ids);

    /**
     * 删除选股方法信息
     * 
     * @param id 选股方法主键
     * @return 结果
     */
    public int deleteFunctionSymbolSelectionById(Long id);
}
