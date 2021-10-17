/*
 * Copyright 2017, OYMotion Inc.
 * All rights reserved.
 *
 * Redistribution and use in source and binary forms, with or without
 * modification, are permitted provided that the following conditions
 * are met:
 *
 * 1. Redistributions of source code must retain the above copyright
 *    notice, this list of conditions and the following disclaimer.
 *
 * 2. Redistributions in binary form must reproduce the above copyright
 *    notice, this list of conditions and the following disclaimer in
 *    the documentation and/or other materials provided with the
 *    distribution.
 *
 * THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
 * "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
 * LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS
 * FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE
 * COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
 * INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
 * BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS
 * OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED
 * AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
 * OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF
 * THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH
 * DAMAGE.
 *
 */

#include "EMGFilters.h"

void EMGFilters::init(SAMPLE_FREQUENCY sampleFreq,
                     NOTCH_FREQUENCY  notchFreq,
                     bool             enableNotchFilter,
                     bool             enableLowpassFilter,
                     bool             enableHighpassFilter) {
    m_sampleFreq   = sampleFreq;
    m_notchFreq    = notchFreq;
    m_bypassEnabled = true;
    if (((sampleFreq == SAMPLE_FREQ_500HZ) || (sampleFreq == SAMPLE_FREQ_1000HZ)) &&
        ((notchFreq == NOTCH_FREQ_50HZ) || (notchFreq == NOTCH_FREQ_60HZ))) {
            m_bypassEnabled = false;
    }

    LPF.init(FILTER_TYPE_LOWPASS, m_sampleFreq);
    HPF.init(FILTER_TYPE_HIGHPASS, m_sampleFreq);
    AHF.init(m_sampleFreq, m_notchFreq);

    m_notchFilterEnabled    = enableNotchFilter;
    m_lowpassFilterEnabled  = enableLowpassFilter;
    m_highpassFilterEnabled = enableHighpassFilter;
}

int EMGFilters::update(int inputValue) {
    int output = 0;
    if (m_bypassEnabled) {
        return output = inputValue;
    }

    // first notch filter
    if (m_notchFilterEnabled) {
        // output = NTF.update(inputValue);
        output = AHF.update(inputValue);
    } else {
        // notch filter bypass
        output = inputValue;
    }

    // second low pass filter
    if (m_lowpassFilterEnabled) {
        output = LPF.update(output);
    }

    // third high pass filter
    if (m_highpassFilterEnabled) {
        output = HPF.update(output);
    }

    return output;
}
