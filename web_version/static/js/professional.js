class ProfessionalFeatures {
    static async generateReport(data) {
        const response = await fetch('/generate_report', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data)
        });
        const blob = await response.blob();
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = 'property_analysis.pdf';
        a.click();
    }

    static async shareAnalysis(email, data) {
        const response = await fetch('/share_analysis', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ email, ...data })
        });
        return response.json();
    }

    static async getQRCode(data) {
        const response = await fetch('/get_qr', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data)
        });
        const blob = await response.blob();
        const url = window.URL.createObjectURL(blob);
        const img = document.createElement('img');
        img.src = url;
        return img;
    }
} 