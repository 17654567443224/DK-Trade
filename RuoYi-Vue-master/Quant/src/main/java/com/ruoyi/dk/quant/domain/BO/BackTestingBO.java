package com.ruoyi.dk.quant.domain.BO;

import com.ruoyi.dk.quant.client.Enum.CryptoInterval;

public class BackTestingBO {
    private Long id;
    private String symbol;
    private String interval;
    private String start;
    private String end;
    // Getter 和 Setter
    public Long getId() {
        return id;
    }

    public void setId(Long id) {
        this.id = id;
    }

    public String getSymbol() {
        return symbol;
    }

    public void setSymbol(String symbol) {
        this.symbol = symbol;
    }

    public String getInterval() {
        return interval;
    }

    public void setInterval(String interval) {
        // 校验 interval 是否是枚举常量对应的字符串值
        boolean isValid = false;
        for (CryptoInterval cryptoInterval : CryptoInterval.values()) {
            if (cryptoInterval.getValue().equals(interval)) {
                isValid = true;
                break;
            }
        }
        if (!isValid) {
            throw new IllegalArgumentException("Invalid interval: " + interval);
        }
        this.interval = interval;
    }

    public String getStart() {
        return start;
    }

    public void setStart(String start) {
        this.start = start;
    }

    public String getEnd() {
        return end;
    }

    public void setEnd(String end) {
        this.end = end;
    }
}
