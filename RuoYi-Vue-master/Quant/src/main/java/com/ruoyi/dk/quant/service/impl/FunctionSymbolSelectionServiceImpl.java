package com.ruoyi.dk.quant.service.impl;

import java.util.List;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import com.ruoyi.dk.quant.mapper.FunctionSymbolSelectionMapper;
import com.ruoyi.dk.quant.domain.FunctionSymbolSelection;
import com.ruoyi.dk.quant.service.IFunctionSymbolSelectionService;

/**
 * 选股方法Service业务层处理
 * 
 * @author ruoyi
 * @date 2025-02-27
 */
@Service
public class FunctionSymbolSelectionServiceImpl implements IFunctionSymbolSelectionService 
{
    @Autowired
    private FunctionSymbolSelectionMapper functionSymbolSelectionMapper;

    /**
     * 查询选股方法
     * 
     * @param id 选股方法主键
     * @return 选股方法
     */
    @Override
    public FunctionSymbolSelection selectFunctionSymbolSelectionById(Long id)
    {
        return functionSymbolSelectionMapper.selectFunctionSymbolSelectionById(id);
    }

    /**
     * 查询选股方法列表
     * 
     * @param functionSymbolSelection 选股方法
     * @return 选股方法
     */
    @Override
    public List<FunctionSymbolSelection> selectFunctionSymbolSelectionList(FunctionSymbolSelection functionSymbolSelection)
    {
        return functionSymbolSelectionMapper.selectFunctionSymbolSelectionList(functionSymbolSelection);
    }

    /**
     * 新增选股方法
     * 
     * @param functionSymbolSelection 选股方法
     * @return 结果
     */
    @Override
    public int insertFunctionSymbolSelection(FunctionSymbolSelection functionSymbolSelection)
    {
        return functionSymbolSelectionMapper.insertFunctionSymbolSelection(functionSymbolSelection);
    }

    /**
     * 修改选股方法
     * 
     * @param functionSymbolSelection 选股方法
     * @return 结果
     */
    @Override
    public int updateFunctionSymbolSelection(FunctionSymbolSelection functionSymbolSelection)
    {
        return functionSymbolSelectionMapper.updateFunctionSymbolSelection(functionSymbolSelection);
    }

    /**
     * 批量删除选股方法
     * 
     * @param ids 需要删除的选股方法主键
     * @return 结果
     */
    @Override
    public int deleteFunctionSymbolSelectionByIds(Long[] ids)
    {
        return functionSymbolSelectionMapper.deleteFunctionSymbolSelectionByIds(ids);
    }

    /**
     * 删除选股方法信息
     * 
     * @param id 选股方法主键
     * @return 结果
     */
    @Override
    public int deleteFunctionSymbolSelectionById(Long id)
    {
        return functionSymbolSelectionMapper.deleteFunctionSymbolSelectionById(id);
    }
}
