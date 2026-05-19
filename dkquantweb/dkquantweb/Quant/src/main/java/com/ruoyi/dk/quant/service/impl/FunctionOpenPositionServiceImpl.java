package com.ruoyi.dk.quant.service.impl;

import java.util.List;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import com.ruoyi.dk.quant.mapper.FunctionOpenPositionMapper;
import com.ruoyi.dk.quant.domain.FunctionOpenPosition;
import com.ruoyi.dk.quant.service.IFunctionOpenPositionService;

/**
 * 开仓方法Service业务层处理
 * 
 * @author ruoyi
 * @date 2025-02-27
 */
@Service
public class FunctionOpenPositionServiceImpl implements IFunctionOpenPositionService 
{
    @Autowired
    private FunctionOpenPositionMapper functionOpenPositionMapper;

    /**
     * 查询开仓方法
     * 
     * @param id 开仓方法主键
     * @return 开仓方法
     */
    @Override
    public FunctionOpenPosition selectFunctionOpenPositionById(Long id)
    {
        return functionOpenPositionMapper.selectFunctionOpenPositionById(id);
    }

    /**
     * 查询开仓方法列表
     * 
     * @param functionOpenPosition 开仓方法
     * @return 开仓方法
     */
    @Override
    public List<FunctionOpenPosition> selectFunctionOpenPositionList(FunctionOpenPosition functionOpenPosition)
    {
        return functionOpenPositionMapper.selectFunctionOpenPositionList(functionOpenPosition);
    }

    /**
     * 新增开仓方法
     * 
     * @param functionOpenPosition 开仓方法
     * @return 结果
     */
    @Override
    public int insertFunctionOpenPosition(FunctionOpenPosition functionOpenPosition)
    {
        return functionOpenPositionMapper.insertFunctionOpenPosition(functionOpenPosition);
    }

    /**
     * 修改开仓方法
     * 
     * @param functionOpenPosition 开仓方法
     * @return 结果
     */
    @Override
    public int updateFunctionOpenPosition(FunctionOpenPosition functionOpenPosition)
    {
        return functionOpenPositionMapper.updateFunctionOpenPosition(functionOpenPosition);
    }

    /**
     * 批量删除开仓方法
     * 
     * @param ids 需要删除的开仓方法主键
     * @return 结果
     */
    @Override
    public int deleteFunctionOpenPositionByIds(Long[] ids)
    {
        return functionOpenPositionMapper.deleteFunctionOpenPositionByIds(ids);
    }

    /**
     * 删除开仓方法信息
     * 
     * @param id 开仓方法主键
     * @return 结果
     */
    @Override
    public int deleteFunctionOpenPositionById(Long id)
    {
        return functionOpenPositionMapper.deleteFunctionOpenPositionById(id);
    }
}
